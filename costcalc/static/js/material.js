document.addEventListener("DOMContentLoaded", function() {  
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const gridElement = document.getElementById('table');
    const newMaterialUrl = gridElement.getAttribute('data-new-material-url');

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

    insertButtonToTableHeader('+', newMaterialUrl);

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
        window.location.href = `/material/${materialId}/edit`;
    }

    function deleteMaterial(materialId, grid) {
        if (confirm(`Are you sure you want to delete material ID ${materialId}?`)) {
            fetch(`/material/${materialId}/delete`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': csrfToken }
            })
            .then(response => {
                if (response.ok) {
                    alert('Material deleted successfully.');
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
