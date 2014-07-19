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
                    'cogenda-app/static/css/cogenda.admin.min.css': ['cogenda-app/static/css/cogenda.admin.css'],
                    'cogenda-app/static/css/cogenda.web.min.css': ['cogenda-app/static/css/cogenda.web.css']
                }
            }
        },
        uglify: {
            dist: {
                files: {
                    'cogenda-app/static/js/cogenda.admin.min.js': ['cogenda-app/static/js/cogenda.admin.js'],
                    'cogenda-app/static/js/cogenda.web.min.js': ['cogenda-app/static/js/cogenda.web.js']
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
        jshint: {
            options: {
                //jshintrc: '.jshintrc'
                browser: true,
                curly: false,
                eqeqeq: true,
                immed: true,
                latedef: true,
                newcap: true,
                noarg: true,
                sub: true,
                undef: true,
                boss: true,
                eqnull: true,
                node: true,
                strict: true,
                es5: false,
                globals: { $: true}
            },
            all: ['cogenda-app/static/js/cogenda.admin.js', 'cogenda-app/static/js/cogenda.web.js','!node_modules/**/*.js', '!test/**/*.js']
        },
        wiredep: {
            web: {
                src: [
                    'cogenda-app/templates/web/layout/layout.html',
                ],
                cwd: '',
                includeSelf: false,
                dependencies: true,
                devDependencies: false,
                exclude: ['bootstrap.css', 'bootstrap-switch', 'jquery-ui', 'datatables', 'select2', 'multiselect', 'quicksearch'],
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
                //exclude: ['mediaelement', 'bxslider-4', 'dataTables.css', 'multi-select.js'],
                exclude: ['mediaelement', 'bxslider-4', 'dataTables.css'],
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
                exclude: ['mediaelement', 'bxslider-4', 'bootstrap-switch', 'jquery-ui', 'datatables', 'select2', 'multiselect', 'quicksearch'],
                fileTypes: {},
                ignorePath: '../../..',
                overrides: {}
            }
        }
    });

    // Load tasks
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-recess');
    grunt.loadNpmTasks('grunt-contrib-imagemin');
    grunt.loadNpmTasks('grunt-wiredep');

    // Register tasks
    grunt.registerTask('jslint', ['jshint']);
    grunt.registerTask('build', ['clean', 'recess', 'uglify', 'imagemin']);
    grunt.registerTask('inject', ['wiredep:web', 'wiredep:admin', 'wiredep:auth']);
};
