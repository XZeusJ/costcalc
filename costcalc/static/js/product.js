document.addEventListener("DOMContentLoaded", function() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const gridElement = document.getElementById('table');
    const newProductUrl = gridElement.getAttribute('data-new-product-url');
    let grid;

    fetchProducts().then(data => initializeGrid(data));

    function fetchProducts() {
        return fetch('/product/get')
            .then(response => response.json())
            .catch(error => console.error('Error fetching products:', error));
    }

    function initializeGrid(data) {
        const gridConfig = {
            columns: getColumns(),
            data: data,
            search: true,
            sort: true,
            pagination: true
        };

        grid = new gridjs.Grid(gridConfig).render(gridElement);
        insertButtonToTableHeader('+', newProductUrl);
    }

    function getColumns() {
        return [
            { id: 'id', name: 'ID' },
            { id: 'name', name: '产品名称' },
            { id: 'material_cost', name: '材料费' },
            { id: 'labor_cost', name: '人工费' },
            { id: 'trans_cost', name: '运输费' },
            { id: 'post_tax_cost', name: '税后' },
            { id: 'total_cost', name: '总成本' },
            {
                name: '操作',
                formatter: (_, row) => createActionButtons(row.cells[0].data)
            }
        ];
    }

    function insertButtonToTableHeader(buttonText, newUrl) {
        const gridHead = document.querySelector('.gridjs-head');
        const gridSearch = document.querySelector('.gridjs-search');

        const buttonWrapper = document.createElement('div');
        buttonWrapper.className = 'button-wrapper';
        buttonWrapper.style.cssText = "float: left; margin-right: 1rem;";

        const newButton = document.createElement('a');
        newButton.className = 'btn btn-primary';
        newButton.href = newUrl;
        newButton.innerText = buttonText;
        buttonWrapper.appendChild(newButton);

        gridHead.insertBefore(buttonWrapper, gridSearch);
    }

    function createActionButtons(productId) {
        return gridjs.h('div', { className: 'action-buttons d-flex' }, [
            createButton('详情', 'btn-info', `/product/${productId}/detail`),
            createButton('编辑', 'btn-primary', `/product/${productId}/edit`),
            createDeleteButton(productId)
        ]);
    }

    function createButton(label, className, href) {
        return gridjs.h('button', {
            className: ` me-1 ${className}`,
            onClick: () => { window.location.href = href; }
        }, label);
    }

    function createDeleteButton(productId) {
        return gridjs.h('button', {
            className: 'btn-danger',
            onClick: () => deleteProduct(productId)
        }, '删除');
    }

    function deleteProduct(productId) {
        if (confirm(`Are you sure you want to delete product ID ${productId}?`)) {
            fetch(`/product/${productId}/delete`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': csrfToken }
            })
            .then(response => {
                if (response.ok) {
                    alert('Product deleted successfully.');
                    grid.updateConfig({ data: grid.config.data.filter(item => item.id !== productId) }).forceRender();
                } else {
                    alert('Failed to delete product.');
                }
            });
        }
    }
});
