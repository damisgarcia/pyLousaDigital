'use strict';

/**
 * @ngdoc directive
 * @name pyLousaDigitalApp.directive:deviceMicrophones
 * @description
 * # deviceMicrophones
 */
angular.module('pyLousaDigitalApp')
  .directive('deviceMicrophones', function () {
    return {
      templateUrl: 'app/templates/device-microphones.html',
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        // 
      }
    };
  });
