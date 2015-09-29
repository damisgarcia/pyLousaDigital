'use strict';

/**
 * @ngdoc function
 * @name pyLousaDigitalApp.controller:MediaDetailCtrl
 * @description
 * # MediaDetailCtrl
 * Controller of the pyLousaDigitalApp
 */
angular.module('pyLousaDigitalApp')
  .controller('MediaDetailCtrl', function ($scope, $stateParams) {
    $scope.media = { id: $stateParams.id }
    $scope.media.video = $scope.repository.media[$stateParams.id]
    $scope.media.thumbnail = $scope.repository.thumbnails[$stateParams.id]
  });
