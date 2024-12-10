// Hàm capitalize chuỗi
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function loadTickets(status) {
    const titles = {
        total: "All Tickets",
        open: "Open Tickets",
        in_progress: "In Progress Tickets",
        closed: "Closed Tickets"
    };

    // Cập nhật tiêu đề modal
    document.getElementById('tickets-title').innerText = titles[status] || "Tickets";

    fetch(`/admin/api/tickets/${status}`)
        .then(response => response.json())
        .then(data => {
            const ticketsBody = document.getElementById('tickets-body');

            // Xóa dữ liệu cũ
            ticketsBody.innerHTML = "";

            // Thêm dữ liệu mới
            if (data.tickets && data.tickets.length > 0) {
                data.tickets.forEach((ticket) => {
                    const row = `
                        <tr class="clickable-row" data-ticket-id="${ticket.id}">
                            <td>${ticket.id}</td>
                            <td>${ticket.title}</td>
                            <td>${ticket.description}</td>
                            <td>
                                <span class="badge 
                                    ${ticket.status === 'new' ? 'bg-info' : 
                                       ticket.status === 'in_progress' ? 'bg-warning text-dark' : 
                                       'bg-success'}">
                                    ${capitalizeFirstLetter(ticket.status.replace('_', ' '))}
                                </span>
                            </td>
                        </tr>`;
                    ticketsBody.innerHTML += row;
                });

                // Thêm sự kiện click vào từng dòng
                document.querySelectorAll('.clickable-row').forEach(row => {
                    row.addEventListener('click', function () {
                        const ticketId = this.getAttribute('data-ticket-id');
                        window.location.href = `/tickets/${ticketId}`;
                    });
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
