angular.module('ViewerApp',[
    'ngCookies'
])
    .controller('ViewerCtrl', ViewerCtrl);


function ViewerCtrl($cookies, $http) {
    var ctrl = this;

    ctrl.user = null;

    ctrl.checkToken = checkToken;
    ctrl.setToken = setToken;

    activate();

    function activate() {
        if (!!checkToken()) {
            $http.get('/user').then(function(resp) {
                ctrl.user = resp.data;
            });
        }

        $http.get('/llama').then(function(resp) {
            ctrl.llamas = resp.data.llamas;
        });
    }

    function checkToken() {
        token = $cookies.get('api_token');
        console.log('Token: ' + token);
        return token;

    }

    function setToken(val) {
        $cookies.put('api_token', val);
        console.log('Set api_token to ' + val);
    }
}
ViewerCtrl.$inject= ['$cookies', '$http'];