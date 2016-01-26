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

      self.form = $("#singin")
      unableField(self.form)

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
      try {
        $rootScope.$profile = data.profile
        $rootScope.$token = data.access_token
      } finally {
        enableField(self.form)
      }
    }

    function onSuccessDestroy(data){
      try{
        $rootScope.$token = null
        $rootScope.$profile = null
      } finally {
        enableField(self.form)
      }
    }

    function onFail(error){
      try{
        if(error.status == 401){
          flash('danger',(error.message || "Acesso não Autorizado: Email ou Senha estão incorretos."))
        }
        else if(error.status == 403){
          flash('danger',(error.message || "Você não possui tal privilégio."))
        }
        else if(error.status == 404){
          flash('danger',(error.message || "Servidor não encontrado aguarde um momente e tente novamente."))
        }
        else if(error.status == 500){
          flash('danger',(error.message || "Falha no servidor error 500."))
        }
        else{
          flash('danger',(error.message || "Error Desconhecido, por favor entre em contato com nossa central de relacionamento."))
        }
      } finally {
        enableField(self.form)
      }
    }

    function unableField(form){
      $(form).find('input,button').each(function(index,ele){
        $(ele).prop('disabled', true)
      })
    }

    function enableField(form){
      $(form).find('input,button').each(function(index,ele){
        $(ele).prop('disabled', false)
      })
    }
  });
