angular.module('LoginApp',[
    'ngCookies'
])
    .controller('LoginCtrl', LoginCtrl);


function LoginCtrl($cookies, $http) {
    var ctrl = this;

    ctrl.user = null;

    ctrl.checkToken = checkToken;
    ctrl.setToken = setToken;
    ctrl.login = login;

    activate();

    function activate() {
        if (!!checkToken()) {
            $http.get('/user').then(function(resp) {
                ctrl.user = resp.data;
            });
        }
    }

    function login(loginForm){
        $http.post('/user/login', loginForm).then(function(resp) {
            ctrl.user = resp.data
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
LoginCtrl.$inject= ['$cookies', '$http'];