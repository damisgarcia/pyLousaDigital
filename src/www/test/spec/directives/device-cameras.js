'use strict';

describe('Directive: deviceCameras', function () {

  // load the directive's module
  beforeEach(module('pyLousaDigitalApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<device-cameras></device-cameras>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the deviceCameras directive');
  }));
});
