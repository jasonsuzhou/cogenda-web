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
        clean: {
            dist: ['cogenda-app/static/css/cogenda.min.css', 'cogenda-app/static/js/cogenda.min.js']
        },
        wiredep: {
            web: {
                src: [
                    'cogenda-app/templates/web/layout/layout.html',
                ],
                cwd: '',
                dependencies: true,
                devDependencies: false,
                exclude: ['bootstrap.css', 'bootstrap-switch', 'jquery-ui', 'datatables', 'select2', 'multiselect'],
                fileTypes: {},
                ignorePath: '../../..',
                overrides: {}
            },

            admin: {
                src: [
                    'cogenda-app/templates/admin/layout/layout-include-js.html',
                    'cogenda-app/templates/admin/layout/layout-include-css.html',
                ],
                cwd: '',
                dependencies: true,
                devDependencies: false,
                exclude: ['mediaelement', 'bxslider-4', 'dataTables.css', 'multi-select.js'],
                fileTypes: {},
                ignorePath: '../../..',
                overrides: {}
            },
            auth: {
                src: [
                    'cogenda-app/templates/admin/security/security-container.html',
                ],
                cwd: '',
                dependencies: true,
                devDependencies: false,
                exclude: ['mediaelement', 'bxslider-4', 'bootstrap-switch', 'jquery-ui', 'datatables', 'select2', 'multiselect'],
                fileTypes: {},
                ignorePath: '../../..',
                overrides: {}
            }
        }
    });

    // Load tasks
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-recess');
    grunt.loadNpmTasks('grunt-contrib-imagemin');
    grunt.loadNpmTasks('grunt-svgmin');
    grunt.loadNpmTasks('grunt-wiredep');
    grunt.loadNpmTasks('grunt-bower-task');

    // Register tasks
    grunt.registerTask('optimize', ['clean', 'recess', 'uglify', 'imagemin']);
    grunt.registerTask('web', ['wiredep:web', 'wiredep:admin', 'wiredep:auth']);
};
