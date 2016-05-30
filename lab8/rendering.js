function getPerspectiveCamera() {
  var camera = new THREE.PerspectiveCamera(
    75, window.innerWidth / window.innerHeight, 0.1, 1000
  );
  camera.position.z = 5;
  camera.up = new THREE.Vector3(0, 1, 0);
  camera.lookAt(new THREE.Vector3(0, 0, 0));

  return camera;
}


function getXYCamera() {
  var ratio = window.innerWidth / window.innerHeight;
  var camera = new THREE.OrthographicCamera(
    -5, 5, 5 / ratio, -5 / ratio, 0.1, 1000
  );
  camera.position.z = 5;
  camera.up = new THREE.Vector3(0, 1, 0);
  camera.lookAt(new THREE.Vector3(0, 0, 0));

  return camera;
}


function getXZCamera() {
  var ratio = window.innerWidth / window.innerHeight;
  var camera = new THREE.OrthographicCamera(
    -5, 5, 5 / ratio, -5 / ratio, 0.1, 1000
  );
  camera.position.y = 5;
  camera.up = new THREE.Vector3(0, 0, 1);
  camera.lookAt(new THREE.Vector3(0, 0, 0));

  return camera;
}


function getYZCamera() {
  var ratio = window.innerWidth / window.innerHeight;
  var camera = new THREE.OrthographicCamera(
    -5, 5, 5 / ratio, -5 / ratio, 0.1, 1000
  );
  camera.position.x = 5;
  camera.up = new THREE.Vector3(0, 0, 1);
  camera.lookAt(new THREE.Vector3(0, 0, 0));

  return camera;
}


function RenderSettings() {
  this.rotationX = 0;
  this.rotationY = 0;
  this.rotationZ = 0;

  this.scaleX = 1;
  this.scaleY = 1;
  this.scaleZ = 1;

  this.translateX = 0;
  this.translateY = 0;
  this.translateZ = 0;

  this.orthoXY = function () {
    this.camera = getXYCamera();
  };
  this.orthoXZ = function () {
    this.camera = getXZCamera();
  };
  this.orthoYZ = function () {
    this.camera = getYZCamera();
  };
  this.perspective = function () {
    this.camera = getPerspectiveCamera();
  };

  this.camera = getPerspectiveCamera();
}


function initGui(settings) {
  var gui = new dat.GUI();

  gui.add(settings, 'rotationX', 0, 359);
  gui.add(settings, 'rotationY', 0, 359);
  gui.add(settings, 'rotationZ', 0, 359);
  gui.add(settings, 'scaleX', 0.1, 5);
  gui.add(settings, 'scaleY', 0.1, 5);
  gui.add(settings, 'scaleZ', 0.1, 5);
  gui.add(settings, 'translateX', -5, 5);
  gui.add(settings, 'translateY', -5, 5);
  gui.add(settings, 'translateZ', -5, 5);
  gui.add(settings, 'orthoXY');
  gui.add(settings, 'orthoXZ');
  gui.add(settings, 'orthoYZ');
  gui.add(settings, 'perspective');

  return gui;
}


function initRenderer() {
  var renderer = new THREE.WebGLRenderer({antialias: true});
  renderer.shadowMapType = THREE.PCFSoftShadowMap;
  renderer.setSize( window.innerWidth, window.innerHeight );
  document.body.appendChild(renderer.domElement);

  return renderer;
}


function initTransformText() {
  var textDiv = document.createElement('div');
  textDiv.style.position = 'absolute';
  textDiv.style.width = 100;
  textDiv.style.height = 100;
  textDiv.style.color = "white";
  textDiv.style.top = 20 + 'px';
  textDiv.style.left = 20 + 'px';
  document.body.appendChild(textDiv);

  return textDiv;
}


function initProjectionText() {
  var textDiv = document.createElement('div');
  textDiv.style.position = 'absolute';
  textDiv.style.width = 100;
  textDiv.style.height = 100;
  textDiv.style.color = "white";
  textDiv.style.bottom = 20 + 'px';
  textDiv.style.left = 20 + 'px';
  document.body.appendChild(textDiv);

  return textDiv;
}


function initCameraText() {
  var textDiv = document.createElement('div');
  textDiv.style.position = 'absolute';
  textDiv.style.width = 100;
  textDiv.style.height = 100;
  textDiv.style.color = "white";
  textDiv.style.bottom = 20 + 'px';
  textDiv.style.right = 20 + 'px';
  document.body.appendChild(textDiv);

  return textDiv;
}


function formatMatrix(matrix) {
  var string = "";
  for (var i = 0; i < 4; ++i) {
    var line = "";
    for (var j = 0; j < 4; ++j) {
      line += Number(matrix.elements[i * 4 + j]).toFixed(2).toString();
      line += (j == 3 ? "" : " ");
    }

    string += line;
    string += (i == 3 ? "" : "<br>");
  }

  return string;
}


function getLetterMesh() {
  var geometry = new THREE.Geometry();
  geometry.vertices.push(
    new THREE.Vector3(0, 0, 0),
    new THREE.Vector3(1, 0, 0),
    new THREE.Vector3(1, -1, 0),
    new THREE.Vector3(0, -1, 0),
    new THREE.Vector3(-1, -2, 0),
    new THREE.Vector3(2, -2, 0),
    new THREE.Vector3(2, 1, 0),
    new THREE.Vector3(0, 1, 0),
    new THREE.Vector3(0, 2, 0),
    new THREE.Vector3(2, 2, 0),
    new THREE.Vector3(2, 3, 0),
    new THREE.Vector3(-1, 3, 0)
  );
  geometry.faces.push(
    new THREE.Face3(0, 1, 7),
    new THREE.Face3(1, 6, 7),
    new THREE.Face3(2, 6, 1),
    new THREE.Face3(2, 5, 6),
    new THREE.Face3(3, 5, 2),
    new THREE.Face3(4, 5, 3),
    new THREE.Face3(4, 3, 11),
    new THREE.Face3(3, 8, 11),
    new THREE.Face3(8, 10, 11),
    new THREE.Face3(8, 9, 10)
  );

  geometry.computeBoundingSphere();

  var material = new THREE.MeshBasicMaterial({color: 0xAAAA00, wireframe: true});
  var letter = new THREE.Mesh(geometry, material);

  return letter;
}


document.addEventListener("DOMContentLoaded", function(event) {
  var settings = new RenderSettings();
  var gui = initGui(settings);
  var renderer = initRenderer();

  var transformText = initTransformText();
  var projectionText = initProjectionText();
  var cameraText = initCameraText();

  var scene = new THREE.Scene();
  var letter = getLetterMesh();
  scene.add(letter);

  var axisHelper = new THREE.AxisHelper(1);
  scene.add(axisHelper);

  var render = function () {
    requestAnimationFrame(render);

    letter.rotation.x = settings.rotationX * Math.PI / 180;
    letter.rotation.y = settings.rotationY * Math.PI / 180;
    letter.rotation.z = settings.rotationZ * Math.PI / 180;

    letter.scale.x = settings.scaleX;
    letter.scale.y = settings.scaleY;
    letter.scale.z = settings.scaleZ;

    letter.position.x = settings.translateX;
    letter.position.y = settings.translateY;
    letter.position.z = settings.translateZ;

    transformText.innerHTML = "Model matrix:<br>" + formatMatrix(letter.matrix);
    projectionText.innerHTML = "Projection matrix:<br>" + formatMatrix(settings.camera.projectionMatrix);
    cameraText.innerHTML = "View matrix:<br>" + formatMatrix(settings.camera.matrixWorldInverse);

    renderer.render(scene, settings.camera);
  };

  render();
});
