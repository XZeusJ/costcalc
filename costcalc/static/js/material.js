document.addEventListener("DOMContentLoaded", function() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const gridElement = document.getElementById('materialTable');
    let grid

    fetchMaterials().then(data => initializeGrid(data));

    document.getElementById('newMaterialForm').addEventListener('submit', function(event) {
        event.preventDefault();
        submitForm(this, '/material/new').then(data => {
            if (data.status === 'success') {
                $('#newMaterialModal').modal('hide');
                addGridRow(data.material);
            } else {
                alert('Error: ' + data.message);
            }
        });
    });

    function fetchMaterials() {
        return fetch('/material/get')
            .then(response => response.json())
            .catch(error => console.error('Error fetching materials:', error));
    }

    function initializeGrid(data) {
        const gridConfig = {
            columns: [
                { id: 'id', name: 'ID' },
                { id: 'name', name: '材料名称' },
                { id: 'spec', name: '材料规格' },
                { id: 'unit_price', name: '单价/g' },
                {
                    name: '操作',
                    formatter: (_, row) => createActionButtons(row.cells[0].data)
                }
            ],
            data: data,
            search: true,
            sort: true,
            pagination: true
        };

        grid = new gridjs.Grid(gridConfig).render(gridElement);
    }

    function submitForm(form, url) {
        const formData = new FormData(form);
        return fetch(url, {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': csrfToken }
        }).then(response => response.json());
    }

    function createActionButtons(materialId) {
        return gridjs.h('div', { className: 'action-buttons' }, [
            createButton('编辑', 'btn-primary', () => editMaterial(materialId)),
            createButton('删除', 'btn-danger', () => deleteMaterial(materialId))
        ]);
    }

    function createButton(text, bgColor, onClick) {
        return gridjs.h('button', {
            className: `${bgColor}`,
            onClick: onClick
        }, text);
    }

    function editMaterial(materialId) {
        fetch(`/material/${materialId}/edit`)
            .then(response => response.text())
            .then(html => {
                const modalBody = document.querySelector('#editMaterialModal .modal-body');
                modalBody.innerHTML = html;
                $('#editMaterialModal').modal('show');
                initEditForm(materialId);
            });
    }

    function initEditForm(materialId) {
        const form = document.querySelector('#editMaterialModal form');
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            submitForm(this, `/material/${materialId}/edit`).then(data => {
                if (data.status === 'success') {
                    $('#editMaterialModal').modal('hide');
                    updateGridRow(data.material);
                } else {
                    alert('Error: ' + data.message);
                }
            });
        });
    }

    function deleteMaterial(materialId) {
        if (confirm(`Are you sure you want to delete material ID ${materialId}?`)) {
            fetch(`/material/${materialId}/delete`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': csrfToken }
            }).then(response => {
                if (response.ok) {
                    grid.updateConfig({ data: grid.config.data.filter(item => item.id !== materialId) }).forceRender();
                } else {
                    alert('Failed to delete material.');
                }
            });
        }
    }

    function addGridRow(material) {
        const newData = [...grid.config.data, material];
        grid.updateConfig({ data: newData }).forceRender();
    }

    function updateGridRow(updatedMaterial) {
        const newData = grid.config.data.map(item => {
            if (item.id === updatedMaterial.id) {
                return { ...item, ...updatedMaterial };
            }
            return item;
        });
        grid.updateConfig({ data: newData }).forceRender();
    }
});
