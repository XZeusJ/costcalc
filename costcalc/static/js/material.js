document.addEventListener("DOMContentLoaded", function() {  
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const gridElement = document.getElementById('materialTable');

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

    const grid = new gridjs.Grid(gridConfig).render(gridElement);


    document.getElementById('newMaterialForm').addEventListener('submit', function(event) {
        event.preventDefault();  // 阻止表单的默认提交行为
        const formData = new FormData(this);
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken  // 确保你的 CSRF token 正确传递
            }
        }).then(response => response.json())
          .then(data => {
            if (data.status === 'success') {
                $('#newMaterialModal').modal('hide');  // 关闭模态框
                const updatedData = [...grid.config.data, data.material]; // 添加新的行到表格,服务器响应包含 material
                grid.updateConfig({
                    data: updatedData
                }).forceRender(); // 强制重新渲染表格
            } else {
                alert('Error: ' + data.message);
            }
        }).catch(error => console.error('Error:', error));
    });
    

    function createActionButtons(materialId) {
        return gridjs.h('div', { className: 'action-buttons' }, [
            createButton('编辑', 'btn-primary', () => editMaterial(materialId)),
            createButton('-', 'btn-danger', () => deleteMaterial(materialId, grid))
        ]);
    }

    function createButton(text, bgColor, onClick) {
        return gridjs.h('button', {
            className: `border rounded-md ${bgColor}`,
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
            initEditForm(materialId); // 初始化表单提交事件
        });
    }

    function initEditForm(materialId) {
        const form = document.querySelector('#editMaterialModal form');
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(this);
            fetch(`/material/${materialId}/edit`, {
                method: 'POST',
                body: formData,
                headers: { 'X-CSRFToken': csrfToken }
            }).then(response => response.json())
              .then(data => {
                if (data.status === 'success') {
                    $('#editMaterialModal').modal('hide');
                    updateGridRow(data.material);  // 更新表格行
                } else {
                    alert('Error: ' + data.message);
                }
            });
        });
    }

    function updateGridRow(updatedMaterial) {
        const newData = grid.config.data.map(item => {
            if (item.id === updatedMaterial.id) {
                return {...item, ...updatedMaterial};
            }
            return item;
        });
        grid.updateConfig({data: newData}).forceRender();
    }

    function deleteMaterial(materialId, grid) {
        if (confirm(`Are you sure you want to delete material ID ${materialId}?`)) {
            fetch(`/material/${materialId}/delete`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': csrfToken }
            })
            .then(response => {
                if (response.ok) {
                    // Optionally, refresh the grid or remove the row
                    const updatedData = grid.config.data.filter(item => item.id !== materialId);
                    grid.updateConfig({ data: updatedData }).forceRender();
                } else {
                    alert('Failed to delete material.');
                }
            });
        }
    }

});
