'use strict';

/**
 * @ngdoc function
 * @author Damis Garcia
 * @name pyLousaDigitalApp.config
 * @description
 * # pyLousaDigitalApp
 */
angular.module('pyLousaDigitalApp',['ui.router'])
  .config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise("/");

    $stateProvider
      .state('media', {
        url: "/",
        templateUrl: "app/views/media.html",
        controller: "MediaCtrl"
      })

      .state('media.detail', {
        url: "/media/:id",
        templateUrl: "app/views/media-detail.html",
        controller: "MediaDetailCtrl"
      })

      .state('lessons', {
        url: "/lessons",
        templateUrl: "app/views/lessons.html"
      })

      .state('account', {
        url: "/account",
        templateUrl: "app/views/account.html"
      })

      .state('settings', {
        url: "/settings",
        templateUrl: "app/views/settings.html"
      })
    })

    .run(function($rootScope,$http){
      $rootScope.$log = []

      $rootScope.$capture = function(){
        $http.get("/capture/new").success(function(data){
          $rootScope.$log.push(data)
        })
      }
    })
