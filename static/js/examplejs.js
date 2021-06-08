const buttonAdd = document.getElementById('addbtn');
const buttonGroup = document.getElementById('group');

buttonAdd.addEventListener("click", addRadio);

function addRadio() {
    console.log("hello");
    var radio = document.createElement('input');
    radio.setAttribute("type", "radio");
    radio.setAttribute("name", "option")
    var text = document.createElement('input');
    text.setAttribute("type", "text");
    text.setAttribute("value", "Option");
    text.setAttribute("class", "opt");
    buttonGroup.appendChild(radio);
    buttonGroup.appendChild(text);
    var br = document.createElement("br");
    buttonGroup.appendChild(br);

}