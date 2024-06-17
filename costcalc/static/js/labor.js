document.addEventListener("DOMContentLoaded", function() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const gridElement = document.getElementById('laborTable');
    let grid;

    fetchLabors().then(data => initializeGrid(data));

    document.getElementById('newLaborForm').addEventListener('submit', function(event) {
        event.preventDefault();
        submitForm(this, '/labor/new').then(data => {
            if (data.status === 'success') {
                $('#newLaborModal').modal('hide');
                addGridRow(data.labor);
            } else {
                alert('Error: ' + data.message);
            }
        });
    });

    function fetchLabors() {
        return fetch('/labor/get')
            .then(response => response.json())
            .catch(error => console.error('Error fetching labors:', error));
    }

    function initializeGrid(data) {

        const gridConfig = {
            columns: [
                { id: 'id', name: 'ID' },
                { id: 'name', name: '工序名称' },
                { id: 'deprec_cost', name: '折旧费用' },
                { id: 'elec_cost', name: '电费' },
                { id: 'labor_cost', name: '人工费用' },
                { id: 'user_name', name: '负责人' },
                {
                    name: '操作',
                    formatter: (_, row) => createActionButtons(row.cells[0].data)
                }
            ],
            data: data,
            search: true,
            sort: true,
        };

        new gridjs.Grid(gridConfig).render(gridElement);
    }

    function submitForm(form, url) {
        const formData = new FormData(form);
        return fetch(url, {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': csrfToken }
        }).then(response => response.json());
    }

    function createActionButtons(laborId) {
        return gridjs.h('div', { className: 'action-buttons' }, [
            createButton('编辑', 'btn-primary', () => editLabor(laborId)),
            createButton('删除', 'btn-danger', () => deleteLabor(laborId))
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
                initEditForm(laborId);
            });
    }

    function initEditForm(laborId) {
        const form = document.querySelector('#editLaborModal form');
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            submitForm(this, `/labor/${laborId}/edit`).then(data => {
                if (data.status === 'success') {
                    $('#editLaborModal').modal('hide');
                    updateGridRow(data.labor);
                } else {
                    alert('Error: ' + data.message);
                }
            });
        });
    }

    function deleteLabor(laborId) {
        if (confirm(`Are you sure you want to delete labor ID ${laborId}?`)) {
            fetch(`/labor/${laborId}/delete`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': csrfToken }
            }).then(response => {
                if (response.ok) {
                    grid.updateConfig({ data: grid.config.data.filter(item => item.id !== laborId) }).forceRender();
                } else {
                    alert('Failed to delete labor.');
                }
            });
        }
    }

    function addGridRow(labor) {
        const newData = [...grid.config.data, labor];
        grid.updateConfig({ data: newData }).forceRender();
    }

    function updateGridRow(updatedLabor) {
        const newData = grid.config.data.map(item => {
            if (item.id === updatedLabor.id) {
                return { ...item, ...updatedLabor };
            }
            return item;
        });
        grid.updateConfig({ data: newData }).forceRender();
    }
});
