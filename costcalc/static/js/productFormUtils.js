// utils.js
var new_productmaterialform_url = "/productmaterial/newform";
var new_productlaborform_url = "/productlabor/newform";

function initializeSelect2WithPlaceholder(newSelect, placeholderText) {
    const emptyOption = document.createElement('option');
    emptyOption.value = "";
    emptyOption.disabled = true;
    emptyOption.selected = true;
    emptyOption.hidden = true;
    newSelect.insertBefore(emptyOption, newSelect.firstChild);

    $(newSelect).select2({
        placeholder: placeholderText,
        allowClear: true,
        width: '100%'
    });
    // 打开时聚焦搜索框
    $(document).on('select2:open', () => {
        document.querySelector('.select2-search__field').focus();
    });
}

function addForm(type, containerId, formCounter) {
    const url = type === 'material' ? new_productmaterialform_url : new_productlaborform_url;
    const container = document.getElementById(containerId);

    fetch(url)
        .then(response => response.text())
        .then(html => {
            formCounter[type]++;
            const newForm = document.createElement('div');
            newForm.innerHTML = html.replace(/__prefix__/g, formCounter[type]);
            const newSelect = newForm.querySelector(`select[name$="-${type}_choices"]`);
            container.appendChild(newForm);
            initializeSelect2WithPlaceholder(newSelect, `Select a ${type}`);
            if (type === 'material') {
                initializeSpecLoading(newForm);
            }
        })
        .catch(error => console.error('Error:', error));
}

function submitForm(form, url, onSuccess, onError) {
    const formData = new FormData(form);
    return fetch(url, {
        method: 'POST',
        body: formData,
        headers: { 'X-CSRFToken': csrfToken }
    }).then(response => response.json())
      .then(data => {
          if (data.status === 'success') {
              onSuccess(data);
          } else {
              onError(data.message);
          }
      });
}

function initializeSpecLoading(formElement) {
    const materialNameSelect = $(formElement).find(`select[name$="-material_choices"]`);
    const specSelect = $(formElement).find(`select[name$="-spec_choices"]`);

    materialNameSelect.on('select2:select', function(e) {
        const materialName = e.params.data.text;
        fetch(`/material/specs?name=${encodeURIComponent(materialName)}`)
            .then(response => response.json())
            .then(specs => {
                let options = '';
                specs.forEach(spec => {
                    options += `<option value="${spec.id}">${spec.spec}</option>`;
                });
                specSelect.html(options);
                specSelect.select2();
            })
            .catch(error => console.error('Error loading specs:', error));
    });
}

function removeForm(button) {
    const formRow = button.closest('.row');
    const productId = document.getElementById('product-form').getAttribute('data-product-id');
    const materialId = formRow.getAttribute('data-material-id');
    const laborId = formRow.getAttribute('data-labor-id');

    if (materialId || laborId) {
        if (confirm('Are you sure you want to delete this item?')) {
            const url = getDeleteUrl(productId, materialId, laborId);
            sendDeleteRequest(url)
                .then(success => {
                    if (success) {
                        formRow.remove();
                    } else {
                        alert('Failed to delete the item.');
                    }
                });
        }
    } else {
        formRow.remove();
    }
}

function getDeleteUrl(productId, materialId, laborId) {
    if (materialId) {
        return `/product/${productId}/material/${materialId}/delete`;
    } else if (laborId) {
        return `/product/${productId}/labor/${laborId}/delete`;
    }
    return null;
}

function sendDeleteRequest(url) {
    return fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token() }}'
        }
    }).then(response => response.ok)
      .catch(error => {
          console.error('Error:', error);
          return false;
      });
}

function addMaterialToSelect2(material) {
    $('select[id*="material_choices"]').each(function() {
        var $select = $(this);
        var newOption = new Option(material.name, material.id, false, false);
        $select.append(newOption).trigger('change'); // 更新 select2 控件并触发 change 事件
    });
}

function addLaborToSelect2(labor) {
    $('select[id*="labor_choices"]').each(function() {
        var $select = $(this);
        var newOption = new Option(labor.name, labor.id, false, false);
        $select.append(newOption).trigger('change'); // 更新 select2 控件并触发 change 事件
    });
}

function checkDuplicatesBeforeSubmit(selectContainerSelector, inputSelector = null) {
    let values = [];
    let isDuplicate = false;

    // 如果有 inputSelector 参数，先处理 input
    if (inputSelector) {
        $(inputSelector).each(function() {
            const inputValue = $(this).val().trim();
            if (values.indexOf(inputValue) !== -1 && inputValue !== "") {
                isDuplicate = true;
                return false; // 有重复，终止循环
            }
            values.push(inputValue);
        });
    }

    // 处理 select
    $(selectContainerSelector + ' select').each(function() {
        const selectedText = $(this).find('option:selected').text().trim();
        if (values.indexOf(selectedText) !== -1 && selectedText !== "") {
            isDuplicate = true;
            return false; // 有重复，终止循环
        }
        values.push(selectedText);
    });

    return isDuplicate;
}
