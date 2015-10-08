'use strict';

/**
 * @ngdoc function
 * @name pyLousaDigitalApp.controller:AccountCtrl
 * @description
 * # AccountCtrl
 * Controller of the pyLousaDigitalApp
 */
angular.module('pyLousaDigitalApp')
  .controller('AccountCtrl', function ($rootScope,$scope,$http,flash) {
    var self = this

    this.singin = function() {
      self.email ? self.not_valid_email = false : self.not_valid_email = true
      self.password ? self.not_valid_password = false : self.not_valid_password = true      

      if(self.email.length == 0 || self.password.length == 0){
        return false
      }

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
      flash('success',"Login efetuado com sucesso")
    }

    function onSuccessDestroy(data){
      $rootScope.$token = null
      $rootScope.$profile = null
      flash('warning',"Sessão Finalizada")
    }

    function onFail(error){
      flash('danger',(error.message || "Não foi possível efetuar login, origem do erro é desconhecida"))
    }
  });
