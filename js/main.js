import SettingsMenu from './src/states/SettingsMenu.js';


var Main = function () {};
var config = {
	type: Phaser.AUTO,
	width: 600,
	height: 400,
	title: "Wordl"
};
var game = new Phaser.Game(config);
var gameOptions = {
	playSound: true,
	playMusic: true
};
var musicPlayer;


Main.prototype = {
	
	preload: function () {
		game.load.script('splash', 'states/Splash.js')
	},

	create: function () {
		game.state.add('Splash', Splash);
		game.state.start('Splash');
	}
};


game.state.add('Main', Main);
game.state.start('Main');