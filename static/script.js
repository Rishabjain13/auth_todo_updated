document.addEventListener("DOMContentLoaded", () => {

    let accessToken = sessionStorage.getItem("access_token");

    const dateEl = document.getElementById("todayDate");
    if (dateEl) {
        dateEl.textContent = new Date().toLocaleDateString("en-IN", {
            day: "numeric",
            month: "short",
            year: "numeric"
        });
    }

    const taskInput = document.getElementById("taskInput");
    const prioritySelect = document.getElementById("prioritySelect");

    const todayTasksBox = document.getElementById("todayTasks");
    const completedTasksBox = document.getElementById("completedTasks");

    const doneCountEl = document.getElementById("doneCount");
    const pendingCountEl = document.getElementById("pendingCount");
    const overdueCountEl = document.getElementById("overdueCount");

    let currentShareTaskId = null;

    async function apiFetch(url, options = {}) {
        options.headers = {
            ...(options.headers || {}),
            Authorization: `Bearer ${accessToken}`
        };

        const res = await fetch(url, options);

        if (res.status === 401) {
            sessionStorage.removeItem("access_token");
            window.location.href = "/login";
        }

        return res;
    }

    async function loadUser() {
        if (!accessToken) {
            window.location.href = "/login";
            return;
        }

        const res = await apiFetch("/me");
        if (!res.ok) return;

        const user = await res.json();
        document.getElementById("username").textContent = user.name;
        document.getElementById("useremail").textContent = user.email;

        sessionStorage.setItem("role", user.role);

        if (user.role === "admin") {
            document.getElementById("adminBtn")?.classList.remove("hidden");
        }
    }

    async function loadTasks() {
        const res = await apiFetch("/tasks");
        if (!res.ok) return;

        const tasks = await res.json();

        todayTasksBox.innerHTML = "";
        completedTasksBox.innerHTML = "";

        let done = 0;
        let pending = 0;


        tasks.forEach(task => {
            const div = document.createElement("div");
            div.className = "task";

            const isOwner = task.permission === "owner";
            const isEditor = task.permission === "editor";
            const isViewer = task.permission === "viewer";

            div.innerHTML = `
                <input type="checkbox"
                    ${task.completed ? "checked" : ""}
                    ${isViewer ? "disabled" : ""}>

                <span class="title">
                    ${task.completed ? `<s>${task.title}</s>` : task.title}
                </span>

                <span class="${task.priority.toLowerCase()}">${task.priority}</span>

                <span class="perm ${task.permission}">
                    ${task.permission.toUpperCase()}
                </span>

                ${isOwner ? `<button class="share">➤</button>` : ``}
                ${(isOwner || isEditor) ? `<button class="edit">✏️</button>` : ``}
                ${isOwner ? `<button class="delete">🗑</button>` : ``}
            `;

            if (!isViewer) {
                div.querySelector("input").addEventListener("change", async () => {
                    await apiFetch(`/tasks/${task.id}`, {
                        method: "PUT",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            title: task.title,
                            priority: task.priority,
                            completed: !task.completed
                        })
                    });
                    loadTasks();
                });
            }

            if (isOwner || isEditor) {
                div.querySelector(".edit")?.addEventListener("click", async () => {
                    const newTitle = prompt("Edit task title", task.title);
                    if (!newTitle) return;

                    const newPriority = prompt(
                        "Edit priority (High / Medium / Low)",
                        task.priority
                    );
                    if (!["High", "Medium", "Low"].includes(newPriority)) return;

                    await apiFetch(`/tasks/${task.id}`, {
                        method: "PUT",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            title: newTitle,
                            priority: newPriority,
                            completed: task.completed
                        })
                    });
                    loadTasks();
                });
            }

            if (isOwner) {
                div.querySelector(".delete")?.addEventListener("click", async () => {
                    await apiFetch(`/tasks/${task.id}`, { method: "DELETE" });
                    loadTasks();
                });

                div.querySelector(".share")?.addEventListener("click", () => {
                    currentShareTaskId = task.id;
                    document.getElementById("shareModal").classList.remove("hidden");
                });
            }

            if (task.completed) {
                done++;
                completedTasksBox.appendChild(div);
            } else {
                pending++;
                todayTasksBox.appendChild(div);
            }
        });

       

        doneCountEl.textContent = done;
        pendingCountEl.textContent = pending;
        overdueCountEl.textContent = 0;
    }

    async function addTask() {
        const title = taskInput.value.trim();
        if (!title) return;

        await apiFetch("/tasks", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                title: title,
                priority: prioritySelect.value,
                completed: false
            })
        });

        taskInput.value = "";
        loadTasks();
    }

    window.shareTask = async function () {
        const email = document.getElementById("shareEmail").value.trim();
        const permission = document.getElementById("sharePermission").value;

        if (!email) return alert("Email required");

        await apiFetch(`/tasks/${currentShareTaskId}/share?user_email=${email}&permission=${permission}`, {
            method: "POST"
        });

        document.getElementById("shareModal").classList.add("hidden");
        document.getElementById("shareEmail").value = "";
        alert("Task shared successfully");
    };

    window.closeShareModal = function () {
        document.getElementById("shareModal").classList.add("hidden");
    };

    window.logout = function () {
        sessionStorage.removeItem("access_token");
        fetch("/logout", { method: "POST" });
        window.location.href = "/login";
    };

    window.addTask = addTask;

    loadUser();
    loadTasks();
});
