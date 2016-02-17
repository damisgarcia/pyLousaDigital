'use strict';

/**
 * @ngdoc directive
 * @name pyLousaDigitalApp.directive:deviceCameras
 * @description
 * # deviceCameras
 */
angular.module('pyLousaDigitalApp')
  .directive('deviceCameras', function () {
    return {
      templateUrl: 'app/templates/device-cameras.html',
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        //
      }
    };
  });
