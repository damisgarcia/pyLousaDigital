'use strict';

/**
 * @ngdoc directive
 * @name pyLousaDigitalApp.directive:horizontalLoader
 * @description
 * # horizontalLoader
 */
angular.module('pyLousaDigitalApp')
  .directive('horizontalLoader', function () {
    return {
      templateUrl: 'app/templates/horizontal-loader.html',
      restrict: 'E'
    };
  });
