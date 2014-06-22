'use strict';
module.exports = function(grunt) {

    grunt.initConfig({
        recess: {
            dist: {
                options: {
                    compile: true,
                    compress: true
                },
                files: {
                    'static/css/cogenda.min.css': ['static/css/*.css']
                }
            }
        },
        uglify: {
            dist: {
                files: {
                    'static/js/cogenda.min.js': ['static/js/cogenda.*.js']
                }
            }
        },
        imagemin: {
            dist: {
                options: {
                    optimizationLevel: 7,
                    progressive: true
                },
                files: [{
                    expand: true,
                    cwd: 'static/images/',
                    src: '{,*/}*.{png,jpg,jpeg}',
                    dest: 'static/images/'
                }]
            }
        },
        svgmin: {
            dist: {
                files: [{
                    expand: true,
                    cwd: 'static/images/',
                    src: '{,*/}*.svg',
                    dest: 'static/images/'
                }]
            }
        },
        clean: {
            dist: ['static/css/cogenda.min.css', 'static/js/cogenda.min.js']
        }
    });

    // Load tasks
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-recess');
    grunt.loadNpmTasks('grunt-contrib-imagemin');
    grunt.loadNpmTasks('grunt-svgmin');

    // Register tasks
    grunt.registerTask('default', ['clean', 'recess', 'uglify', 'imagemin', 'svgmin']);
};
