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
                    'cogenda-app/static/css/cogenda.min.css': ['cogenda-app/static/css/*.css']
                }
            }
        },
        uglify: {
            dist: {
                files: {
                    'cogenda-app/static/js/cogenda.min.js': ['cogenda-app/static/js/cogenda.*.js']
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
                    cwd: 'cogenda-app/static/images/',
                    src: '{,*/}*.{png,jpg,jpeg}',
                    dest: 'cogenda-app/static/images/'
                }]
            }
        },
        svgmin: {
            dist: {
                files: [{
                    expand: true,
                    cwd: 'cogenda-app/static/images/',
                    src: '{,*/}*.svg',
                    dest: 'cogenda-app/static/images/'
                }]
            }
        },
        clean: {
            dist: ['cogenda-app/static/css/cogenda.min.css', 'cogenda-app/static/js/cogenda.min.js']
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
