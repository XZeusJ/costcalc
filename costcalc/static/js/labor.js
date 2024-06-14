document.addEventListener("DOMContentLoaded", function() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const gridElement = document.getElementById('laborTable');

    const gridConfig = {
        columns: [
            { id: 'id', name: 'ID', sort: { enabled: true, direction: 'desc' } },
            { id: 'name', name: '人工名称' },
            { id: 'deprec_cost', name: '设备折旧' },
            { id: 'elec_cost', name: '电费CNY/H' },
            { id: 'labor_cost', name: '人工CNY/H' },
            { name: '操作', formatter: (_, row) => createActionButtons(row.cells[0].data) }
        ],
        data: data,
        search: true,
        sort: true,
        pagination: true
    };

    const grid = new gridjs.Grid(gridConfig).render(gridElement);

    document.getElementById('newLaborForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': csrfToken }
        }).then(response => response.json())
          .then(data => {
            if (data.status === 'success') {
                $('#newLaborModal').modal('hide');
                const updatedData = [...grid.config.data, data.labor];
                grid.updateConfig({ data: updatedData }).forceRender();
            } else {
                alert('Error: ' + data.message);
            }
        }).catch(error => console.error('Error:', error));
    });

    function createActionButtons(laborId) {
        return gridjs.h('div', { className: 'action-buttons' }, [
            createButton('编辑', 'btn-primary', () => editLabor(laborId)),
            createButton('-', 'btn-danger', () => deleteLabor(laborId, grid))
        ]);
    }

    function createButton(text, bgColor, onClick) {
        return gridjs.h('button', {
            className: `border rounded-md ${bgColor}`,
            onClick: onClick
        }, text);
    }

    function editLabor(laborId) {
        fetch(`/labor/${laborId}/edit`)
        .then(response => response.text())
        .then(html => {
            const modalBody = document.querySelector('#editLaborModal .modal-body');
            modalBody.innerHTML = html;
            $('#editLaborModal').modal('show');
            initEditForm(laborId); // 初始化表单提交事件
        });
    }

    function initEditForm(laborId) {
        const form = document.querySelector('#editLaborModal form');
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(this);
            fetch(`/labor/${laborId}/edit`, {
                method: 'POST',
                body: formData,
                headers: { 'X-CSRFToken': csrfToken }
            }).then(response => response.json())
              .then(data => {
                if (data.status === 'success') {
                    $('#editLaborModal').modal('hide');
                    updateGridRow(data.labor);  // 更新表格行
                } else {
                    alert('Error: ' + data.message);
                }
            }).catch(error => console.error('Error:', error));
        });
    }

    function updateGridRow(updatedLabor) {
        const newData = grid.config.data.map(item => {
            if (item.id === updatedLabor.id) {
                return {...item, ...updatedLabor};
            }
            return item;
        });
        grid.updateConfig({ data: newData }).forceRender();
        insertAddButton();
    }

    function deleteLabor(laborId, grid) {
        if (confirm(`Are you sure you want to delete labor ID ${laborId}?`)) {
            fetch(`/labor/${laborId}/delete`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': csrfToken }
            })
            .then(response => {
                if (response.ok) {
                    alert('Labor deleted successfully.');
                    const updatedData = grid.config.data.filter(item => item.id !== laborId);
                    grid.updateConfig({ data: updatedData }).forceRender();
                } else {
                    alert('Failed to delete labor.');
                }
            }).catch(error => console.error('Error:', error));
        }
    }
});
