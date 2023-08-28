let medicines = document.querySelectorAll(".medicines")
let container = document.querySelector("#medicines")
let addButton = document.querySelector("#add-form")
let removeButton = document.querySelectorAll(".remove-form")
let totalForms = document.querySelector("#id_form-TOTAL_FORMS")

let formNum = medicines.length-1
addButton.addEventListener('click', addForm)

function removeButtonEventListener(disabled = false) {
  removeButton.forEach(function(button){
    button.addEventListener('click', removeForm)
    button.setAttribute('disabled', true);
    if (disabled == false) {
      button.removeAttribute('disabled');
    }
  })
}

removeButtonEventListener(disabled = formNum == 0)

function addForm(e) {
  e.preventDefault()

  let newForm = medicines[0].cloneNode(true)
  let formRegex = RegExp(`form-(\\d){1}-`,'g')

  formNum++

  newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
  container.insertBefore(newForm, addButton)
  if (newForm.querySelector(`input[name=form-${formNum}-id]`) != null) {
    newForm.querySelector(`input[name=form-${formNum}-id]`).value = 0
  }
  newForm.querySelector('input[type=text]').value = ''
  newForm.querySelector('input[type=number]').value = ''
  totalForms.setAttribute('value', `${formNum+1}`)
  removeButton = document.querySelectorAll(".remove-form")
  if (formNum) {
    removeButtonEventListener(disabled = false);
  }
}

function removeForm(e) {
  e.preventDefault()

  let elSelector = e.target.getAttribute('data-id')
  let medicine = document.getElementsByClassName(elSelector)
  let deleteButton = document.getElementById(elSelector.replace('-name', '-delete'));
  medicine[0].style.display = 'none'
  deleteButton.value = 1

  formNum = formNum-1

  if (formNum == 0) {
    let firstButton = document.querySelector(`button[data-id=id_form-${formNum}-name]`)
    firstButton.setAttribute('disabled', true);
  }
}
