var app = angular.module('doc_portal_app', []);

// configure the module to use a different template interpolation sequence to avoid conflicting with Django
app.config(function ($interpolateProvider) {
    'use strict';
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

// configure the module to perform C.S.R.F. operations nicely with Django
app.config(['$httpProvider', function ($httpProvider) {
    'use strict';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.service('doc_portal_service', ['$http', function ($http) {
    'use strict';
    this.get_users = function () {
        return $http.get('/api/users/').then(function (response) {
            return response.data;
        });
    };
    this.get_units = function () {
        return $http.get('/api/units/').then(function (response) {
            return response.data;
        });
    };
    this.get_docs = function () {
        return $http.get('/api/documents/').then(function (response) {
            return response.data;
        });
    };
    this.post_user = function (username) {
        return $http.post('/api/users/', {'username': username}).then(function (response) {
            return response.data;
        });
    };
    this.post_unit = function (unit_name) {
        return $http.post('/api/units/', {'name': unit_name}).then(function (response) {
            return response.data;
        });
    };
    this.post_doc = function (doc_name, doc_type, doc_unit) {
        return $http.post('/api/documents/', {
            'name': doc_name,
            'doc_type': doc_type,
            'unit': doc_unit
        }).then(function (response) {
            return response.data;
        });
    };
    this.delete_doc = function (id) {
        return $http.delete('/api/documents/' + id + '/').then(function (response) {
            return response.data;
        });
    };
    this.delete_unit = function (id) {
        return $http.delete('/api/units/' + id + '/').then(function (response) {
            return response.data;
        });
    };
    this.add_document_access = function (document, user) {
        return $http.put('/api/documents/add_access/', {document: document, user: user}).then(function (response) {
            return response.data;
        });
    };
    this.add_unit_access = function (unit, user) {
        return $http.put('/api/units/add_access/', {unit: unit, user: user}).then(function (response) {
            return response.data;
        });
    };
    this.get_document = function (document, user) {
        return $http({
            url: '/access/',
            method: 'GET',
            params: {doc: document, user: user}
        }).then(function (response) {
            return response.data;
        });
    };
}]);

app.controller('doc_portal_controller', ['$scope', 'doc_portal_service', function ($scope, doc_portal_service) {
    'use strict';

    $scope.error_message = '';

    $scope.refresh_users = function () {
        $scope.clear_notifications();
        doc_portal_service.get_users().then(
            function (response) {
                $scope.users = response;
            }
        ).catch(function () {
            $scope.users = [];
            $scope.error_message = 'Could not get users!';
        });
    };

    $scope.refresh_units = function () {
        $scope.clear_notifications();
        doc_portal_service.get_units().then(
            function (response) {
                $scope.units = response;
            }
        ).catch(function () {
            $scope.units = [];
            $scope.error_message = 'Could not get units!';
        });
    };

    $scope.refresh_docs = function () {
        $scope.clear_notifications();
        doc_portal_service.get_docs().then(
            function (response) {
                $scope.docs = response;
            }
        ).catch(function () {
            $scope.docs = [];
            $scope.error_message = 'Could not get documents!';
        });
    };

    $scope.add_user = function () {
        $scope.clear_notifications();
        if (!$scope.new_username) {
            $scope.error_message = 'Invalid username';
            return;
        }
        doc_portal_service.post_user($scope.new_username).then(
            function (response) {
                $scope.info_message = 'Added user ' + $scope.new_username + ' with no password';
                $scope.refresh_users();
            }
        ).catch(function () {
            $scope.error_message = 'Could not create new user!';
        });
    };

    $scope.add_unit = function () {
        $scope.clear_notifications();
        if (!$scope.new_unit_name) {
            $scope.error_message = 'Invalid unit name';
            return;
        }
        doc_portal_service.post_unit($scope.new_unit_name).then(
            function (response) {
                $scope.info_message = 'Added unit ' + $scope.new_unit_name;
                $scope.refresh_units();
            }
        ).catch(function () {
            $scope.error_message = 'Could not create new unit!';
        });
    };

    $scope.add_doc = function () {
        $scope.clear_notifications();
        if (!$scope.new_doc_name) {
            $scope.error_message = 'Invalid doc name!';
            return;
        }
        console.log("About to try to create a document with name, type, unit:", $scope.new_doc_name, $scope.new_doc_type, $scope.new_doc_unit);
        doc_portal_service.post_doc($scope.new_doc_name, $scope.new_doc_type, $scope.new_doc_unit).then(
            function (response) {
                $scope.info_message = 'Added document ' + $scope.new_doc_name;
                $scope.refresh_docs();
            }
        ).catch(function () {
            $scope.error_message = 'Could not create new doc!';
        });
    };

    $scope.delete_doc = function (id, name) {
        $scope.clear_notifications();
        if (!window.confirm("Are you sure you want to delete document: " + name + "?")) {
            return;
        }
        doc_portal_service.delete_doc(id).then(
            function (response) {
                $scope.info_message = 'Deleted doc: ' + name;
                $scope.refresh_all();
            }
        ).catch(function () {
            $scope.error_message = 'Could not delete doc!';
        });
    };

    $scope.delete_unit = function (id, name) {
        $scope.clear_notifications();
        if (!window.confirm("Are you sure you want to delete unit: " + name + "?")) {
            return;
        }
        doc_portal_service.delete_unit(id).then(
            function (response) {
                $scope.info_message = 'Deleted unit: ' + name;
                $scope.refresh_all();
            }
        ).catch(function () {
            $scope.error_message = 'Could not delete doc!';
        });
    };

    $scope.grant_unit = function () {
        $scope.clear_notifications();
        if (!$scope.grant_access_unit) {
            $scope.error_message = 'Select a unit for which to grant access!';
            return;
        }
        if (!$scope.grant_access_user) {
            $scope.error_message = 'Select a user for which to authorize access!';
            return;
        }
        doc_portal_service.add_unit_access($scope.grant_access_unit, $scope.grant_access_user).then(
            function (response) {
                $scope.info_message = 'Added access to unit';
                $scope.refresh_all();
            }
        ).catch(function () {
            $scope.error_message = 'Could not add access to unit!';
        });
    };

    $scope.grant_doc = function () {
        $scope.clear_notifications();
        if (!$scope.grant_access_document) {
            $scope.error_message = 'Select a document for which to grant access!';
            return;
        }
        if (!$scope.grant_access_user) {
            $scope.error_message = 'Select a user for which to authorize access!';
            return;
        }
        doc_portal_service.add_document_access($scope.grant_access_document, $scope.grant_access_user).then(
            function (response) {
                $scope.info_message = 'Added access to document';
                $scope.refresh_all();
            }
        ).catch(function () {
            $scope.error_message = 'Could not add access to document!';
        });
    };

    $scope.test_access = function () {
        doc_portal_service.get_document($scope.test_access_document, $scope.test_access_user).then(
            function (response) {
                $scope.access_message = 'Access Granted!';
            }
        ).catch(function (error) {
            if (error.status === 403) {
                $scope.access_message = 'Access Denied!';
            } else {
                $scope.error_message = 'Problem testing document access';
            }
        });
    };

    $scope.clear_notifications = function () {
        $scope.access_message = '';
        $scope.error_message = '';
        $scope.info_message = '';
    };

    $scope.refresh_all = function () {
        $scope.refresh_users();
        $scope.refresh_units();
        $scope.refresh_docs();
    };

    $scope.init = function () {
        $scope.clear_notifications();
        $scope.doc_types = [
            {'id': '00', 'name': 'UserManual'},
            {'id': '01', 'name': 'ProgressPhotos'},
            {'id': '02', 'name': 'TestingResults'}
        ];
        $scope.refresh_all();
    };

    $scope.init();
}]);