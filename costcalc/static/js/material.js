document.addEventListener("DOMContentLoaded", function() {  
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    // 初始化 Grid.js 表格，并返回 grid 对象
    const grid = new gridjs.Grid({
        columns: [
        { id: 'id', name: 'ID'},
        { id: 'name', name: '材料名称' },
        { id: 'spec', name: '材料规格' },
        { id: 'unit_price', name: '单价/g'},
        { 
            name: '操作',
            formatter: (cell, row) => {
                const materialId = row.cells[0].data;
                return gridjs.h('div', { className: 'action-buttons' }, [
                    gridjs.h('button', {
                        className: 'border rounded-md bg-blue-600',
                        onClick: () => window.location.href = `/material/${materialId}/edit`
                    }, '编辑'),
                    gridjs.h('button', {
                        className: 'border rounded-md bg-red-600',
                        onClick: () => {
                            if (confirm(`Are you sure you want to delete material ID ${materialId}?`)) {
                                // Implement delete functionality here
                                // For example, send a DELETE request to the server
                                fetch(`/material/${materialId}/delete`, {
                                    method: 'DELETE',
                                    headers: {
                                        'X-CSRFToken': csrfToken
                                    }
                                })
                                .then(response => {
                                    if (response.ok) {
                                        alert('Material deleted successfully.');
                                        // Optionally, refresh the grid or remove the row
                                        updatedData = data.filter(item => item.id !== materialId);
                                        grid.updateConfig({ data: updatedData }).forceRender();
                                    } else {
                                        alert('Failed to delete material.');
                                    }
                                });
                            }
                        }
                    }, '删除')
                ]);
            }
        },
        ],
        data: data,
        search: true,
        sort: true,
        pagination: true,
    }).render(document.getElementById('table'));

})


