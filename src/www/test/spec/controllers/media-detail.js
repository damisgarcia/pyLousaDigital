'use strict';

describe('Controller: MediaDetailCtrl', function () {

  // load the controller's module
  beforeEach(module('pyLousaDigitalApp'));

  var MediaDetailCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    MediaDetailCtrl = $controller('MediaDetailCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(MediaDetailCtrl.awesomeThings.length).toBe(3);
  });
});
