var Splash = function () {};

Splash.prototype = {

	loadScripts: function () {
		//game.load.script('style', 'lib/style.js');
		//game.load.script('mixins', 'lib/mixins.js');
		//game.load.script('WebFont', '../webfontloader.js');
		game.load.script('gamemenu','./GameMenu.js');
		game.load.script('game', './Game.js');
		game.load.script('gameover','./GameOver.js');
		game.load.script('credits', './Credits.js');
		game.load.script('options', './Options.js');
	},

	loadBgm: function () {
		//game.load.audio('dangerous', 'static/bgm/Dangerous.mp3');
	},
	
	loadImages: function () {
		//game.load.image('menu-bg', 'static/images/menu-bg.jpg');
	},

	loadFonts: function () {
		WebFontConfig = {
			custom: {
				families: ['TheMinion'],
				urls: ['../../static/style/theminion.css']
			}
		}
	},

	init: function () {
		this.loadingBar = game.make.sprite(game.world.centerX-(387/2), 400, "loading");
		//this.logo = game.make.sprite(game.world.centerX, 200, 'brand');
		this.status = game.make.text(game.world.centerX, 380, 'Loading...', {fill: 'white'});
		utils.centerGameObjects([this.logo, this.status]);
	},

	preload: function () {
		game.add.existing(this.logo).scale.setTo(0.5);
		game.add.existing(this.loadingBar);
		game.add.existing(this.status);
		this.load.setPreloadSprite(this.loadingBar);

		this.loadScripts();
		this.loadImages();
		//this.loadFonts();
		this.loadBgm();
	},

	addGameStates: function () {
		game.state.add("GameMenu",GameMenu);
		game.state.add("Game",Game);
		game.state.add("GameOver",GameOver);
		game.state.add("Credits",Credits);
		game.state.add("Options",Options);
	},

	addGameMusic: function () {
		music = game.add.audio('dangerous');
		music.loop = true;
		music.play();
	},

	create: function() {
		this.status.setText('Ready!');
		this.addGameStates();
		//this.addGameMusic();

		setTimeout(function () {
			game.state.start("GameMenu");
		}, 1000);
	}
};