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
      .state('galerie', {
        url: "/",
        templateUrl: "app/views/galerie.html"
      })

      .state('lessons', {
        url: "/",
        templateUrl: "app/views/lessons.html"
      })

      .state('account', {
        url: "/",
        templateUrl: "app/views/account.html"
      })

      .state('settings', {
        url: "/",
        templateUrl: "app/views/settings.html"
      })
  });
