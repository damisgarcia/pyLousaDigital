'use strict';

/**
 * @ngdoc function
 * @author Damis Garcia
 * @name pyLousaDigitalApp.config
 * @description
 * # pyLousaDigitalApp
 */
angular.module('pyLousaDigitalApp',['ui.router','flash','ngTagsInput'])
  .config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise("/index")
    $stateProvider
      .state('media', {
        url: "/index",
        views: {
          "yield": {
            templateUrl: "app/views/media.html",
            controller: "MediaCtrl"
          }
        }
      })


      .state('media.edit', {
        url: "/media/:id/edit",
        views: {
          "dialog": {
            templateUrl: "app/views/media-lesson-edit.html",
            controller: "MediaEditCtrl"
          }
        }
      })

      .state('media.upload', {
        url: "/media/:id/upload",
        views: {
          "dialog": {
            templateUrl: "app/views/media-lesson-upload.html",
            controller: "MediaUploadCtrl as mediaUploadCtrl"
          }
        }
      })

      .state('capture',{
        views: {
          "dialog":{
            url:"/capture/start",
            templateUrl: "app/templates/dialog-start-record.html"
          }
        }
      })

      .state('account', {
        url: "/account",
        views: {
          "yield": {
            templateUrl: "app/views/account.html",
            controller: "AccountCtrl as account"
          }
        }
      })

      .state('settings', {
        url: "/settings",
        views: {
          "yield": {
            templateUrl: "app/views/settings.html",
            controller: "SettingsCtrl as settingsCtrl"
          }
        }
      })
    })

    .directive('dialogStartRecord',function(){
      return {
        restrict: "E",
        templateUrl:"app/templates/dialog-start-record.html"
      }
    })
