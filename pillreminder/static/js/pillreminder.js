let medicines = document.querySelectorAll(".medicines")
let container = document.querySelector("#medicines")
let addButton = document.querySelector("#add-form")
let removeButton = document.querySelector("#remove-form")
let totalForms = document.querySelector("#id_form-TOTAL_FORMS")

let formNum = medicines.length-1
addButton.addEventListener('click', addForm)
removeButton.addEventListener('click', removeForm)

function addForm(e) {
  e.preventDefault()

  let newForm = medicines[0].cloneNode(true)
  let formRegex = RegExp(`form-(\\d){1}-`,'g')

  formNum++
  newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
  container.insertBefore(newForm, addButton)

  totalForms.setAttribute('value', `${formNum+1}`)
}

function removeForm(e) {
  e.preventDefault()
  let allMedicines = document.querySelectorAll(".medicines")
  let indexToRemove = allMedicines.length - 1
  allMedicines[0].parentElement.removeChild(allMedicines[indexToRemove])
  formNum++
  totalForms.setAttribute('value', `${formNum-1}`)
}
