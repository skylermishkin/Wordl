var MenuItem = new Phaser.Class({
	Extends: Phaser.GameObjects.Text,

	initialize: function MenuItem(x, y, text, scene) {
		Phaser.GameObjects.Text.call(this, scene, x, y, text, 
			{color: '#ffffff', align: 'left', fontSize: 15});
	},

	select: function() {
		
	}
});

var Menu = new Phaser.Class({
	Extends: Phaser.GameObjects.Container,

	initialize: function Menu(x, y, scene) {
		Phaser.GameObjects.Container.call(this, scene, x, y);
		this.menuItems = [];
	}

	addMenuItem: function(text) {
		var menuItem = new MenuItem(0, this.menuItems.length * 20, text, this.scene);
		this.menuItems.push(menuItem);
		this.add(menuItem);	
	},

	confirm: function() {

	}
});