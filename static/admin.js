const token = sessionStorage.getItem("access_token");
const role = sessionStorage.getItem("role");

if (!token || role !== "admin") {
    alert("Unauthorized");
    location.href = "/";
}

async function apiFetch(url, options = {}) {
    return fetch(url, {
        ...options,
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
}


async function loadAdminInfo() {
    const res = await apiFetch("/me");
    const user = await res.json();

    document.getElementById("username").textContent = user.name;
    document.getElementById("useremail").textContent = user.email;
}


async function showStats() {
    const users = await (await apiFetch("/admin/users")).json();
    const tasks = await (await apiFetch("/admin/tasks")).json();

    adminTitle.textContent = "System Overview";

    adminData.innerHTML = `
        <div class="admin-card">👥 Total Users: ${users.length}</div>
        <div class="admin-card">📋 Total Tasks: ${tasks.length}</div>
        <div class="admin-card">✅ Completed Tasks: ${tasks.filter(t => t.completed).length}</div>
        <div class="admin-card">🔄 Shared Tasks: ${tasks.filter(t => t.shared_count > 0).length}</div>
    `;
}

async function loadUsers() {
    const users = await (await apiFetch("/admin/users")).json();

    adminTitle.textContent = "All Users";

    adminData.innerHTML = users.map(u => `
        <div class="admin-card">
            <b>${u.name}</b><br>
            ${u.email}<br>
            Role: <b>${u.role}</b>
        </div>
    `).join("");
}

async function loadAdminTasks() {
    const search = document.getElementById("searchInput")?.value.trim();

    let url = "/admin/tasks";
    if (search) {
        url += `?search=${encodeURIComponent(search)}`;
    }

    const res = await apiFetch(url);
    const tasks = await res.json();

    adminTitle.textContent = "All Tasks";

    if (!tasks.length) {
        adminData.innerHTML = "<p>No tasks found</p>";
        return;
    }

    adminData.innerHTML = tasks.map(t => `
        <div class="admin-card">
            <b>${t.title}</b><br>
            Owner: <b>${t.owner_email}</b><br>
            Priority: ${t.priority}<br>
            Completed: ${t.completed ? "Yes" : "No"}<br>

            <div class="shared-section">
                ${
                    t.shared_with.length
                        ? t.shared_with.map(s =>
                            `<span class="badge shared">
                                ${s.user_email} (${s.permission.toUpperCase()})
                             </span>`
                          ).join(" ")
                        : `<span class="badge owner">Not Shared</span>`
                }
            </div>

            <br>
            <button class="danger" onclick="deleteTask(${t.id})">
                🗑 Delete
            </button>
        </div>
    `).join("");
}


async function deleteTask(taskId) {
    if (!confirm("Are you sure you want to delete this task?")) return;

    await apiFetch(`/admin/tasks/${taskId}`, { method: "DELETE" });
    loadAdminTasks();
}


function logout() {
    sessionStorage.clear();
    location.href = "/login";
}


loadAdminInfo();
showStats();
