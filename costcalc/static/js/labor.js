document.addEventListener("DOMContentLoaded", function() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const gridElement = document.getElementById('table');
    const newLaborUrl = gridElement.getAttribute('data-new-labor-url');


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
                formatter: (_, row) => createActionButtons(row.cells[0].data)
            }
        ],
        data: data,
        search: true,
        sort: true,
        pagination: true
    }).render(gridElement);

    insertButtonToTableHeader('+', newLaborUrl);

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

    function createActionButtons(laborId) {
        return gridjs.h('div', { className: 'action-buttons' }, [
            createButton('编辑', 'btn-primary', () => editLabor(laborId)),
            createButton('-', 'btn-danger', () => deleteLabor(laborId))
        ]);
    }

    function createButton(text, bgColor, onClick) {
        return gridjs.h('button', {
            className: `border rounded-md ${bgColor}`,
            onClick: onClick
        }, text);
    }

    function editLabor(laborId) {
        window.location.href = `/labor/${laborId}/edit`;
    }

    function deleteLabor(laborId) {
        if (confirm(`Are you sure you want to delete labor ID ${laborId}?`)) {
            fetch(`/labor/${laborId}/delete`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => {
                if (response.ok) {
                    alert('Labor deleted successfully.');
                    grid.updateConfig({ data: grid.config.data.filter(item => item.id !== laborId) }).forceRender();
                } else {
                    alert('Failed to delete labor.');
                }
            });
        }
    }
});
