// Javascript file for Recast

window.onload = prepareLinks;

function prepareLinks(){

    /* Called after page load */
    return;
}


function RecastAddParameterPoint(e){
    /* Adds parameter point on the Add Request page. */

    alert("Add parameter point funcction");
    return;
}

function validateFloatValues(val) {
    
    //return false if the value is not float
    return;
}

function validateIntValues(val) {
    
    /* return false if value is not of type integer */
    return;
}

function validateString(val) {
    /* return false if value is not of type string, otherwise true */
    return;
}

function hideshow(attribute_id){

    document.getElementById(attribute_id).classList.add('hide');
}

function RecastValidateExtension(e){

    /* Validates the extension for the zip file to be uploaded */
    var file = e.target.files;
    var fileExtension = theFile.split('.')[theFile.split('.').length - 1].toLowerCase();
    var fileSize = file.size;
    var txt = "";
    if (!(fileExtension == validFileExtension)){
	txt += "file type extension not allowed \n";
	txt += "ONly zip files are allowed";	
    }

    if (fileSize > validFileSize){
	txt += "File size must be less than";
	txt += (validFileSize/1000);
	txt += "MB";
    }
    //do something with the txt variable
}

/* Search panel stuff */

function addLoadEvent(func) {
    /* Load function */
    var oldonload = window.onload;
    if ( typeof window.onload != 'function') {
	window.onload = func;
    }else {
	windown.onload = function() {
	    oldonload();
	    func();
	}
    }
}

function insertAfter(newElement, targetElement){
    var parent = targetElement.parentNode;
    if (parent.lastChild == targetElement){
	parent.appendChild(newElement);
    }else{
	parent.insertBefore(newElement, targetElement.nextSibling);
    }
}

function getElementByClassName(node, classname){
    /* For older browsers  */
    if (node.getElementByClassName) {
	//use the existing method
	return node.getElementByClassName(classname);
    }
    else{
	var results = new Array();
	var elems = node.getElementsByTagName("*");
	for (var i=0; i < elems.length; i++){
	    if (elems[i].classname.indexOf(classname) != -1) {
		results[results.length] = elems[i];
	    }
	}
    }
}

function prepareArxivRequest(id){
    if (id) return arxiv(id);
}

function arxiv(arxiv_id){
    /* Ajax method to query the Arxiv API
         Results still need to be serialized */

    base_url = 'http://export.arxiv.org/api/query?search_query=' + arxiv_id;
    var request = new XMLHttpRequest();
    if (request) {
	request.open("GET", base_url, true);
	request.onreadystatechange = function() {
	    if (request.readyState == 4) {
		var para = document.createElement("p");
		var txt = document.createTextNode(request.responseText);
		para.appendChild(txt);
		document.getElementById('new').appendChild(para);
	    }
	};
	request.send(null);
    }
}