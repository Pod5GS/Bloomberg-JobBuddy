Array.prototype.remove = function () {
    var what, a = arguments, L = a.length, ax;
    while (L && this.length) {
        what = a[--L];
        while ((ax = this.indexOf(what)) !== -1) {
            this.splice(ax, 1);
        }
    }
    return this;
};
var data = [
    {name: "Finance", color: 0xffec4d},
    {name: "Marketing", color: 0xffec4d},
    {name: "Software", color: 0xffec4d},
    {name: "Writing blog posts", color: 0xffec4d},
    {name: "Mobile apps", color: 0xffec4d},
    {name: "Writing blog posts", color: 0xffec4d},
    {name: "Building a web stie", color: 0xffec4d},
    {name: "Experience Design", color: 0xffec4d},
    {name: "Art", color: 0xffec4d},
    {name: "Fasion", color: 0xffec4d},
    {name: "Games", color: 0xffec4d},
    {name: "Film", color: 0xffec4d},
    {name: "Business", color: 0xffec4d}
]
var zoom = 100;
var balls = [];
var activedata = [];
var renderer = PIXI.autoDetectRenderer(window.innerWidth, 450, {
    transparent: true, antialias: true
});
document.getElementById("board").appendChild(renderer.view);
var world = new p2.World({gravity: [0, 0]});
var stage = new PIXI.Container();
stage.position.x = renderer.width / 2; // center at origin
stage.position.y = renderer.height / 1.5;
stage.scale.x = zoom;  // zoom in
stage.scale.y = -zoom; // Note: we flip the y axis to make "up" the physics "up"
//floor
planeShape = new p2.Plane();
planeBody = new p2.Body({position: [0, -1]});
planeBody.addShape(planeShape);
world.addBody(planeBody);


var Ball = function (t, c, r, x) {
    this.init = function () {
        this.el = new PIXI.Container();
        this.baseRadius = this.radius = r;
        this.iscliked = false;
        this.circle = new PIXI.Graphics();
        this.circle.beginFill(c);
        this.circle.drawCircle(0, 0, 0.99);
        this.circle.endFill();
        this.circle.interactive = true;
        this.circle.hitArea = new PIXI.Circle(0, 0, 1);
        this.circle.scale.x = this.circle.scale.y = this.radius;
        this.el.addChild(this.circle);
        this.text = t;
        stage.addChild(this.el);
        let text = new PIXI.Text(t, {
            fontFamily: 'Arial',
            fontSize: 14,
            fill: 0x000000,
            align: 'center',
            wordWrap: true
        });
        text.anchor.x = 0.5;
        text.anchor.y = 0.5;
        text.position.x = 0;
        text.scale.x = 0.01;
        text.scale.y = -0.01;
        this.el.addChild(text);
        this.shape = new p2.Circle({radius: this.radius});
        let startX = x % 2 === 0 ? 2 + r : -2 - r;
        let startY = r - Math.random() * (r * 2);
        this.body = new p2.Body({
            mass: 0.001,
            position: [startX, startY],
            angularVelocity: 0,
            fixedRotation: true
        });
        this.body.addShape(this.shape);
        world.addBody(this.body);
    }
    this.update = function () {
        this.body.applyForce([-this.body.position[0] / 100, -this.body.position[1] / 100]);

        this.el.position.x = this.body.position[0];
        this.el.position.y = this.body.position[1];
        this.el.rotation = this.body.angle;
    }
    this.mouseover = function () {

    }
    this.mouseout = function () {

    }
    this.click = function () {
        if (this.iscliked) {
            this.radius = this.baseRadius;
            TweenMax.to(this.circle.scale, 0.2, {
                x: this.radius,
                y: this.radius,
                onUpdate: this.updateRadius.bind(this),
                onComplete: this.updateRadius.bind(this)
            });
            this.iscliked = false;
            activedata.remove(this.text);
        } else {
            this.radius = this.baseRadius + 0.2;
            TweenMax.to(this.circle.scale, 0.2, {
                x: this.radius,
                y: this.radius,
                onUpdate: this.updateRadius.bind(this),
                onComplete: this.updateRadius.bind(this)
            });
            this.iscliked = true;
            activedata.push(this.text);
        }
    }
    this.updateRadius = function () {
        this.shape.radius = this.circle.scale.x;
        this.body.updateBoundingRadius();
    }
    this.init.call(this);
    this.circle.mouseover = this.mouseover.bind(this);
    this.circle.mouseout = this.mouseout.bind(this);
    this.circle.click = this.click.bind(this);
}
function pushball(){
    for (var i = 0; i < data.length; i++) {
        var ball = new Ball(data[i].name, data[i].color, 0.5, i);
        balls.push(ball);
    }
}

function animate() {
    world.step(1 / 60);
    for (var i = 0; i < this.balls.length; i++) {
        balls[i].update();
    }
    renderer.render(stage);
    requestAnimationFrame(animate);
}

function render(){
    pushball();
    animate();
}

render();

function gotonextbubble() {
    data = [
        {name: "Python", color: 0xffec4d},
        {name: "Ruby", color: 0xffec4d},
        {name: "Javascript", color: 0xffec4d},
        {name: "React", color: 0xffec4d},
        {name: "Angular", color: 0xffec4d},
        {name: "HTML", color: 0xffec4d},
        {name: "CSS", color: 0xffec4d},
        {name: "RESTful", color: 0xffec4d},
        {name: "Bootstrap", color: 0xffec4d},
        {name: "Git", color: 0xffec4d},
        {name: "jQuery", color: 0xffec4d}
    ];
    renderer = PIXI.autoDetectRenderer(window.innerWidth, 450, {
        transparent: true, antialias: true
    });
    document.getElementById("board2").appendChild(renderer.view);
    world = new p2.World({gravity: [0, 0]});
    stage = new PIXI.Container();
    stage.position.x = renderer.width / 2; // center at origin
    stage.position.y = renderer.height / 1.5;
    stage.scale.x = zoom;  // zoom in
    stage.scale.y = -zoom; // Note: we flip the y axis to make "up" the physics "up"
//floor
    planeShape = new p2.Plane();
    planeBody = new p2.Body({position: [0, -1]});
    planeBody.addShape(planeShape);
    world.addBody(planeBody);
    render();
    $('#skillsetsArea').hide();
    $('#step1').attr('class', 'btn btn-default btn-circle');
    $('#step2').attr('class', 'btn btn-primary btn-circle');
    $('#skillsetsArea2').show();
}

function gotosignup() {
    $('#skillsetsArea2').hide();
    $('#step2').attr('class', 'btn btn-default btn-circle');
    $('#step3').attr('class', 'btn btn-primary btn-circle');
    $('#form').show();
}

function recommend() {
    $('#steps').hide();
    $('#form').hide();
    $('#matched').show();
    setTimeout(function(){
        $('#loading').hide();
        $('#results').show();
    }, 4000);
}

$.validator.setDefaults( {
    submitHandler: function () {
        recommend();
    }
} );

$( document ).ready( function () {
    $( "#signupForm" ).validate( {
        rules: {
            name: "required",
            pwd: {
                required: true,
                minlength: 5
            },
            repwd: {
                required: true,
                minlength: 5,
                equalTo: "#pwd"
            },
            email: {
                required: true,
                email: true
            }
        },
        messages: {
            name: "Please enter your name",
            pwd: {
                required: "Please provide a password",
                minlength: "Your password must be at least 5 characters long"
            },
            repwd: {
                required: "Please provide a password",
                minlength: "Your password must be at least 5 characters long",
                equalTo: "Please enter the same password as above"
            },
            email: "Please enter a valid email address",
        },
        errorElement: "em",
        errorPlacement: function ( error, element ) {
            // Add the `help-block` class to the error element
            error.addClass( "validation" );

            if ( element.prop( "type" ) === "checkbox" ) {
                error.insertAfter( element.parent( "label" ) );
            } else {
                error.insertAfter( element );
            }
        },
        highlight: function ( element, errorClass, validClass ) {
            $( element ).parents( ".col-sm-5" ).addClass( "has-error" ).removeClass( "has-success" );
        },
        unhighlight: function (element, errorClass, validClass) {
            $( element ).parents( ".col-sm-5" ).addClass( "has-success" ).removeClass( "has-error" );
        }
    } );
});
