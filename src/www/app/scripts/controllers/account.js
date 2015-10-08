'use strict';

/**
 * @ngdoc function
 * @name pyLousaDigitalApp.controller:AccountCtrl
 * @description
 * # AccountCtrl
 * Controller of the pyLousaDigitalApp
 */
angular.module('pyLousaDigitalApp')
  .controller('AccountCtrl', function ($rootScope,$scope,$http) {
    var self = this

    this.singin = function() {
      var url = "/auth/singin"
      var params = "?email="+this.email+"&password="+this.password
      url += params

      $http({
          url: url,
          dataType: "json",
          method: "GET",
          headers: {
            "Content-Type": "application/json"
          }
        }).success(onSuccessSingin).error(onFail)
    }

    this.destroy = function(){
      var url = "/auth/token/destroy"
      self.isProcessing = true
      $http.get(url).success(onSuccessDestroy).error(onFail)
    }

    // privates
    function onSuccessSingin(data){
      $rootScope.$profile = data.profile
      $rootScope.$token = data.access_token
      $rootScope.$fails = data
    }

    function onSuccessDestroy(data){
      $rootScope.$token = null
      $rootScope.$profile = null
    }

    function onFail(error){
      $rootScope.$fails = error
    }
  });
