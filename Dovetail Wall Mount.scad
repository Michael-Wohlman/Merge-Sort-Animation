
/* [ Wall Mount Plate ] */
// How many screw holes on wall mount plate
screw_holes = 2; // [0,2,4,6]

// How thick is the head of the screws (mm)
screw_thickness = 5; // [0:10]

// The diameter of the screw's long pointy part (mm)
screw_diameter = 2; // [0:10]

// Width of the wall mount plate (mm)
plate_width = 100; //[20:100]

// Height of the wall mount plate (mm)
plate_height = 30; // [10:100]

// Depth of the wall mount plate (mm)
plate_depth = 15; // [1:100]

// Offset of the plate corner curves
plate_offset = 5; // [0:20]

/* [ Dovetail ] */
// Vertical angle ongle of the dovetail mount (degrees, 0 = vertical)
dovetail_vertical_angle = 10; // [0:30]

// width of base of dovetail mount (mm, 0 = no base, should not be more than plate_height)
dovetail_base = 10; // [0:100]

// Width of the dovetail outside hole (mm)
dovetail_outer_width = 70; // [10:90]

// width of inner side of dovetail, against the back of the plate. Should be between plate width and outer width. (mm)
dovetail_inner_width = 85; // [10:99]

// Depth of the dovetail hole. Should be less than plate depth (mm)
dovetail_depth = 10; // [1:99]



/* [ Other ] */
// clearence (mm)
clearence = 0.1; // [0:1]

/* [ Hidden ] */

module WallMount() {

    difference() {
        // Main Block
        translate([0,0,plate_height/2])
        rotate([0,90,90])
        linear_extrude(height=plate_depth)
        offset(r=plate_offset)
        offset(r=-plate_offset)
        square([plate_height,plate_width], center=true);
        
        // Dovetail
        DoveTail(clearence);
        
        // Screw Indent
        translate([0,dovetail_depth,plate_height/2 + dovetail_base,])
        cube([dovetail_inner_width/2, screw_thickness, plate_height], center=true);
        
        // Screw Holes
        for (i=[1:2]) {
            rotate([90,0,0])
            translate([
            0,
            dovetail_base + (((plate_height - dovetail_base)/3)*i),
            -plate_depth/2
            ])
            cylinder(h=plate_depth, r=screw_diameter + clearence, center = true);
            
        };
        
    };
};

module DoveTail(clear) {
    
    points = [
    [dovetail_outer_width/2 + clear, 0, dovetail_base - clear], //FR 0
    [-dovetail_outer_width/2 - clear, 0, dovetail_base - clear], //FL 1
    [-dovetail_inner_width/2 - clear, dovetail_depth + clear, dovetail_base -clear], //BL2
    [dovetail_inner_width/2 + clear, dovetail_depth + clear, dovetail_base - clear], //BR3
    [dovetail_outer_width/2 + clear, 0, plate_height], //FRT 4
    [-dovetail_outer_width/2 - clear, 0, plate_height], //FLT 5
    [-dovetail_inner_width/2 - clear, dovetail_depth+clear, plate_height], //BLT6
    [dovetail_inner_width/2 + clear, dovetail_depth + clear, plate_height] //BRT7
    ];
    
    faces = [
    [0,1,2,3],
    [0,1,5,4],
    [1,2,6,5],
    [2,3,7,6],
    [0,3,7,4],
    [4,5,6,7]
    ];
    
    polyhedron(points, faces);
    
}

WallMount();
