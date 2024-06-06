document.addEventListener("DOMContentLoaded", function() {  
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    const grid = new gridjs.Grid({
        columns: [
        { id: 'id', name: 'ID'},
        { id: 'name', name: '产品名称' },
        { id: 'material_cost', name: '材料费' },
        { id: 'labor_cost', name: '人工费' },
        { id: 'trans_cost', name: '运输费' },
        { id: 'pre_tax_cost', name: '税前' },
        { id: 'post_tax_cost', name: '税后' },
        { 
            name: '操作',
            formatter: (cell, row) => {
                const productId = row.cells[0].data;
                return gridjs.h('div', { className: 'action-buttons' }, [
                    gridjs.h('button', {
                        className: 'border rounded-md bg-blue-600',
                        onClick: () => window.location.href = `/product/${productId}/detail`
                    }, '详情'),
                    gridjs.h('button', {
                        className: 'border rounded-md bg-blue-600',
                        onClick: () => window.location.href = `/product/${productId}/edit`
                    }, '编辑'),
                    gridjs.h('button', {
                        className: 'border rounded-md bg-red-600',
                        onClick: () => {
                            if (confirm(`Are you sure you want to delete product ID ${productId}?`)) {
                                // Implement delete functionality here
                                // For example, send a DELETE request to the server
                                fetch(`/product/${productId}/delete`, {
                                    method: 'DELETE',
                                    headers: {
                                        'X-CSRFToken': csrfToken
                                    }
                                })
                                .then(response => {
                                    if (response.ok) {
                                        alert('Product deleted successfully.');
                                        // Optionally, refresh the grid or remove the row
                                        updatedData = data.filter(item => item.id !== productId);
                                        grid.updateConfig({ data: updatedData }).forceRender();
                                    } else {
                                        alert('Failed to delete product.');
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
