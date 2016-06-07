// Javascript file for Recast

//angular App
angular.module('recastApp', ['ngSanitize'])
    .controller('HomeCtrl', ['$http', '$interval', function($http, $interval) {
	/* home page controller */
	var self = this;
	self.analyses = "-";
	self.requests = "-";
	
	$http.get('/homestats')
	    .then(function(response) {
		self.analyses = response.data.analyses;
		self.requests = response.data.requests;
	    });
	
	
	
	$interval( function() {	    
	    $http.get('/homestats')
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

    .directive('bindHtmlCompile', ['$compile', function($compile) {
	/* Directive that compiles binded html
	   allows ng-click and other similar directives to fire on binded html
	   source:
	   https://github.com/incuna/angular-bind-html-compile/blob/master/angular-bind-html-compile.js
	*/
	return {
	    restrict: 'A',
	    link: function (scope, element, attrs) {
		scope.$watch(function () {
		    return scope.$eval(attrs.bindHtmlCompile);
		}, function (value) {
		    // In case value is a TrustedValueHolderType, sometimes it
		    // needs to be explicitly called into a string in order to
		    // get the HTML string.
		    element.html(value && value.toString());
		    // If scope is provided use it, otherwise use parent scope
		    var compileScope = scope;
		    if (attrs.bindHtmlScope) {
			compileScope = scope.$eval(attrs.bindHtmlScope);
		    }
		    $compile(element.contents())(compileScope);
		});
	    }
	};

    }])
    
    .controller('parameterCtrl', ['$http', 'IDService', 'ItemService', function($http, ris, coordinates) {
	/* Controller to add parameter */
	var self = this;

	self.items = function() {
	    return coordinates.items();
	};

	self.addCoordinate = function() {
	    coordinates.push();
	};

	self.addParameter = function(rid) {
	    ris.setID(rid);
	    coordinates.clear();
	    coordinates.push();
	    $('#modal-add-parameter').modal('show');	    
	};

	self.submit = function() {
	    self.hideModal();
	    NProgress.start();
	    var form_data = new FormData();
	    //form_data.append('file', self.zipFile);

	    for (var k in self.items()){
		parameter = {};
		parameter.name = self.items()[k].name;
		parameter.value = self.items()[k].value;
		par = angular.toJson(parameter);
		form_data.append(k, par);
	    }
	    NProgress.inc(0.4);
	    
	    $http({
		method: 'POST',
		url:'/add-parameter/'+ris.getID(),
		data: form_data,		
		headers: {'Content-Type': undefined},
		transformRequest: angular.identity
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


    .controller('BasicRequestCtrl', ['$http', 'IDService', function($http, prs) {
	/* Controller to add file on request page */
	var self = this;
	self.addBasicRequest = function(pid) {
	    console.log('add basic request modal');	   
	    prs.setID(pid);
	    $('#zip-file-request-page').val('');
	    $('#modal-add-basic-request').modal('show');
	};

	    
	self.submit = function() {
	    self.hideModal();
	    NProgress.start();	    
	    var form_data = new FormData();
	    form_data.append('file', self.zipFile);
	    NProgress.inc(0.4);
	    
	    $http({
		'method': 'POST',
		url: '/add-basic-request/'+prs.getID(),
		data: form_data,
		headers: {'Content-Type': undefined},
		transformRequest: angular.identity
	    })
		.success(function(response){
		    NProgress.inc(0.5);
		    NProgress.done();		   
		    location.reload();
		})
		.error(function(err){
		    NProgress.done();
		});
	};

	self.hideModal = function() {
	    $('#modal-add-basic-request').modal('hide');
	};
    }])

    .controller('showParameterCtrl', ['$http', 'DataService', 'IDService', function($http, ajaxresponse, parameterIndex) {
	/* controller to show parameter data on request page */

	var self = this;
	ajaxresponse.set("");
	parameterIndex.setID(0);
	
	self.mydata = function() {
	    return ajaxresponse.get();
	};

	self.parNumber = function() {
	    return parameterIndex.getID();
	};
	
	self.showParameter = function(uuid, index) {
	    NProgress.start();
	    NProgress.inc(0.4);
	    ajaxresponse.set("<h3>Loading...</h3>");
	    parameterIndex.setID(index);
	    NProgress.inc(0.3);
	    $http.get('/parameter-data/'+uuid)
		.success(function(response) {
		    NProgress.inc(0.5);
		    NProgress.done();		    
		    ajaxresponse.set(response.data);
		    console.log(response.data);
		})
		.error(function(err) {
		    NProgress.done();
		    //error handling
		});	    
	};

    }])

    .controller('ParameterResponseCtrl', ['$http', 'DataService', function($http, ajaxresponse){
	/* Controller to fecth Point response data */
	var self = this;
	//ajaxresponse.set("");
	//ajaxresponse.clear();
	//ajaxresponse.setresponsedata("this is a test");
	//console.log("logging");
	self.mydata = function() {
	    //return response.get();
	    return ajaxresponse.getresponsedata();
	};

	self.hideresponse = function() {
	    NProgress.start();
	    NProgress.inc(0.7);	    
	    NProgress.done();
	    return ajaxresponse.hide();
	};

	self.fetchresponse = function(uuid) {
	    NProgress.start();
	    NProgress.inc(0.4);
	    ajaxresponse.clear();
	    $http.get('/pointresponse-data/'+uuid)
		.success(function(response) {
		    NProgress.inc(0.5);
		    NProgress.done();
		    console.log("fetched response data");
		    //ajaxresponse.set
		    ajaxresponse.setresponsedata(response.data);
		    ajaxresponse.show();
		})
		.error(function(err) {
		    //error handling
		});
	};
	
    }])


    .controller('coordinateCtrl', ['$http', 'IDService', function($http, prs) {
	/* Controller to add coordinate on request page */
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
	    $('#modal-add-coordinate').modal('hide');
	};
    }])


    .controller('arxivImportCtrl', ['$http', 'IDService', function($http, id_service) {
	
	var self = this;
	self.arxiv_id;
	self.example = "this";
	self.here = "hello";
	self.title = "";
	self.collaboration = "";
	self.doi = "";
	self.abstract = "";
	
	self.import = function() {
	    console.log("clicked");
	    console.log(self.arxiv_id);
	    $('#modal-arxiv-data').modal('show');
	    $http.post('/arxiv?id='+self.arxiv_id)
		.then(function(response) {
		    console.log(response);
		    self.title = response.data['title'];
		    self.collaboration = response.data['collaboration'];
		    self.doi = response.data['doi'];
		    self.abstract = response.data['description'];	
		    console.log(self.title);
		    console.log(self.collaboration);
		    console.log(self.doi);
		    console.log(self.abstract);
		});
	};
    }])

    .factory('ItemService', [function() {
	/* list stateful service */
	items = [];
	return {
	    push: function() {
		items.push({
		    name: "",
		    value: "",
		    namePlaceholder: "Name",
		    valuePlaceholder: "Value",
		});
	    },
	    clear: function() {
		items = [];
	    },
	    items: function() {
		return items;
	    }
	}
    }])

    .factory('DataService', [function() {
	mydata = "";
	responsedata = {show: 0, data: ""};
	return {
	    get: function() {
		return mydata;
	    },
	    set: function(val) {
		mydata = val;
	    },
	    show: function() {
		responsedata.show = 1;
	    },
	    hide: function() {
		responsedata.show = 0;
	    },
	    getresponsedata: function() {
		if (responsedata.show){
		    return responsedata.data;
		}else {
		    return "";
		}
	    },
	    setresponsedata: function(mydata) {
		responsedata.data = mydata;
	    },
	    clear: function() {
		responsedata.show = 0;
		responsedata.data = "";
	    }	   
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
