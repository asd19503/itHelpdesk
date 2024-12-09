function loadTickets(status) {
    const titles = {
        total: "All Tickets",
        open: "Open Tickets",
        in_progress: "In Progress Tickets",
        closed: "Closed Tickets"
    };

    // Cập nhật tiêu đề trong modal
    document.getElementById('tickets-title').innerText = titles[status] || "Tickets";

    // Gửi yêu cầu AJAX tới API
    fetch(`/admin/api/tickets/${status}`)
        .then(response => response.json())
        .then(data => {
            const ticketsBody = document.getElementById('tickets-body');

            // Xóa dữ liệu cũ trong bảng
            ticketsBody.innerHTML = "";

            // Thêm dữ liệu mới vào bảng
            if (data.tickets && data.tickets.length > 0) {
                data.tickets.forEach((ticket) => {
                    const row = `<tr>
                        <td>${ticket.id}</td>
                        <td>${ticket.title}</td>
                        <td>${ticket.description}</td>
                        <td>${ticket.status}</td>
                    </tr>`;
                    ticketsBody.innerHTML += row;
                });
            } else {
                ticketsBody.innerHTML = `<tr><td colspan="4" class="text-center">No tickets found.</td></tr>`;
            }

            // Hiển thị modal
            const modal = new bootstrap.Modal(document.getElementById('ticketsModal'));
            modal.show();
        })
        .catch(error => console.error('Error loading tickets:', error));
}
