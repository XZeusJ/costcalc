document.addEventListener("DOMContentLoaded", function() {  
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    // 初始化 Grid.js 表格，并返回 grid 对象
    const grid = new gridjs.Grid({
        columns: [
        { id: 'id', name: 'ID'},
        { id: 'name', name: '工序名称' },
        { id: 'deprec_cost', name: '折旧费用' },
        { id: 'elec_cost', name: '电费' },
        { id: 'labor_cost', name: '人工费用' },
        { 
            name: '操作',
            formatter: (cell, row) => {
                const laborId = row.cells[0].data;
                return gridjs.h('div', { className: 'action-buttons' }, [
                    gridjs.h('button', {
                        className: 'border rounded-md bg-blue-600',
                        onClick: () => window.location.href = `/labor/${laborId}/edit`
                    }, '编辑'),
                    gridjs.h('button', {
                        className: 'border rounded-md bg-red-600',
                        onClick: () => {
                            if (confirm(`Are you sure you want to delete labor ID ${laborId}?`)) {
                                // Implement delete functionality here
                                // For example, send a DELETE request to the server
                                fetch(`/labor/${laborId}/delete`, {
                                    method: 'DELETE',
                                    headers: {
                                        'X-CSRFToken': csrfToken
                                    }
                                })
                                .then(response => {
                                    if (response.ok) {
                                        alert('Labor deleted successfully.');
                                        // Optionally, refresh the grid or remove the row
                                        updatedData = data.filter(item => item.id !== laborId);
                                        grid.updateConfig({ data: updatedData }).forceRender();
                                    } else {
                                        alert('Failed to delete labor.');
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