// Javascript file for Recast

//angular App
angular.module('recastApp', [])
    .controller('HomeCtrl', ['$http', '$interval', function($http, $interval) {
	var self = this;
	self.analyses = 0;
	self.requests = 0;
	
	$interval( function() {
	    $http.get('/analysis-number')
		.then(function(response) {
		    self.analyses = response.data.analyses;
		    self.requests = response.data.requests;
		});
	},3000);
    }])

    .directive('fileModel', ['$parse', function($parse) {
	/* Directive to allow to easily upload a  file
	   using AngularJS $http service, and provides 
	   binding to angular file directive 
	     source: 
	     https://uncorkedstudios.com/blog/multipartformdata-file-upload-with-angularjs
	     */  
	return {
            restrict: 'A',
            link: function(scope, element, attrs) {
		var model = $parse(attrs.fileModel);
		var modelSetter = model.assign;

		element.bind('change', function(){
		    console.log('change');
                    scope.$apply(function(){
			modelSetter(scope, element[0].files[0]);
                    });
		});
            }
	};
    }])

    
    .controller('parameterCtrl', ['$http', 'IDService', function($http, ris) {
	var self = this;
	self.addParameter = function(rid) {
	    ris.setID(rid);
	    $('#zip-file-request-page').val('');
	    $('#modal-add-parameter').modal('show');	    
	};
	self.submit = function() {
	    self.hideModal();
	    NProgress.start();
	    NProgress.inc(0.4);
	    var form_data = new FormData();
	    form_data.append('file', self.zipFile);
	    for (var k in self.parameter){
		form_data.append(k, self.parameter[k]);
	    }
	    $http({
		method: 'POST',
		url:'/add-parameter/'+ris.getID(),
		data: form_data,		
		headers: {'Content-Type': undefined},
		trnasformRequest: angular.identity
	    })
		.success(function(response){
		    NProgress.inc(0.5);
		    self.parameter = {};
		    NProgress.done();
		    location.reload();
		})
		.error(function(err){
		    NProgress.done();
		});
	};
	self.hideModal = function() {
	    $('#modal-add-parameter').modal('hide');
	};
    }])

    .controller('coordinateCtrl', ['$http', 'IDService', function($http, prs) {
	var self = this;
	self.addCoordinate = function(pid) {
	    prs.setID(pid);
	    $('#modal-add-coordinate').modal('show');	    
	};
	self.submit = function() {
	    self.hideModal();
	    NProgress.start();
	    NProgress.inc(0.4);
	    $http.post('/add-coordinate/'+prs.getID(), self.coordinate)
		.then(function(reponse) {
		    NProgress.inc(0.5);
		    self.coordinate = {};
		    NProgress.done();		    
		    location.reload();
		});
	};
	self.hideModal = function() {
	    console.log('hide modal');
	    $('#modal-add-coordinate').modal('hide');
	};
    }])

    .factory('IDService', [function() {
	/* Service to store ID's */
	variable_id = 0;
	return {
	    setID: function(ID) {
		variable_id = ID;
	    },
	    getID: function() {
		return variable_id;
	    }
	};	     
    }]);


    


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

function shortStr(str, max_chars, min_thresh=10){
    /* returns shortened string  */
    if (str.length > min_thresh){
	return (str.substring(0, max_chars)+"...");
    }else{
	return str;
    }
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
    base_url = 'https://inspirehep.net/search?p='+arxiv_id+'&of=recjson';
    console.log('javascript');
    var request = new XMLHttpRequest();
    if (request) {
	request.open("GET", base_url, true);
	request.onreadystatechange = function() {
	    if (request.readyState == 4) {
		//var para = document.createElement("p");
		//var txt = document.createTextNode(request.responseText);
		//para.appendChild(txt);
		//document.getElementById('new').appendChild(para);
		console.log(request.responseText);
	    }
	};
	request.send(null);
    }
}
