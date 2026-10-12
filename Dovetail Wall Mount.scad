
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


/* [ Male Mount ] */

// Thickness of male mounting plate (mm)
male_plate_depth = 5; // [2:20]

// Width of male mounting plate (mm)
male_plate_width = 100; // [20:150]

// Height of male mounting plate (mm)
male_plate_height = 30; // [10:100]

// Number of screw holes
male_screw_holes = 2; // [0,2,4,6]

// Diameter of screw holes (mm)
male_screw_diameter = 3; // [1:10]

// Distance of screw holes from plate edges (mm)
male_screw_inset = 10; // [5:30]


/* [ Other ] */
// Clearance between the two dovetail pieces (mm)
clearence = 0.2; // [0:0.05:1]

// Display mode
display_mode = "Separated"; // [Together, Separated, Wall Mount, Male Mount]

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

// Second half of the dovetail mount





module MaleMount() {

    difference() {

        union() {

            // Male dovetail
            DoveTail(-clearence);

            // Rounded backing plate
            // Clearance affects width and height,
            // but the plate stays connected to the dovetail
            translate([
                0,
                clearence,
                plate_height/2
            ])
            rotate([90,0,0])
            linear_extrude(
                height=male_plate_depth + clearence
            )
            offset(r=plate_offset)
            offset(r=-plate_offset)
            square([
                male_plate_width - 2*clearence,
                male_plate_height - 2*clearence
            ], center=true);
        }

        // Screw holes in backing plate
        if (male_screw_holes > 0) {

            for (i=[0:male_screw_holes-1]) {

                x_pos =
                    -(male_plate_width - 2*clearence)/2 +
                    male_screw_inset +
                    i * (
                        (male_plate_width -
                        2*clearence -
                        2*male_screw_inset) /
                        max(1,male_screw_holes-1)
                    );

                // Through holes
                translate([
                    x_pos,
                    -male_plate_depth/2,
                    plate_height/2
                ])
                rotate([90,0,0])
                cylinder(
                    h=male_plate_depth + 2*clearence + 2,
                    d=male_screw_diameter,
                    center=true,
                    $fn=64
                );
            }
        }
    }
}







/* [ Display ] */

if (display_mode == "Together") {

    color("LightGray")
    WallMount();

    color("Orange")
    MaleMount();

}
else if (display_mode == "Separated") {

    color("LightGray")
    WallMount();

    translate([plate_width + 20, 0, 0])
    color("Orange")
    MaleMount();

}
else if (display_mode == "Wall Mount") {

    WallMount();

}
else if (display_mode == "Male Mount") {

    MaleMount();

}
else {

    // Fallback to avoid empty geometry
    WallMount();

}


