angular.module('MarketApp',[
    'ngCookies'
])
    .controller('MarketCtrl', MarketCtrl);


function MarketCtrl($cookies, $http, $scope) {
    var ctrl = this;

    ctrl.user = null;
    ctrl.llamaCount = null;

    ctrl.buy = buy;
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
            ctrl.llamaCount = resp.data.llamas.length;
        });
    }

    function buy() {
        var cash = ctrl.user.cash - 100;
        $http.put('/cash/' + cash).then(function() {
            ctrl.user.cash = cash;
            return $http.post('/llama');
        }).then(function() {
            ctrl.llamaCount += 1;
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
MarketCtrl.$inject= ['$cookies', '$http', '$scope'];