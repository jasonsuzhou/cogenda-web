'use strict';
module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        concat: {
            options: {
                stripBanners: true,
                banner: '/*! <%= pkg.name %> - v<%= pkg.version %> - ' + '<%= grunt.template.today("yyyy-mm-dd") %> */',
            },
            vendor_js_admin: {
                src: [
                    'cogenda_app/static/js/jquery.js',
                    'cogenda_app/static/js/jquery-ui.js',
                    'cogenda_app/static/js/bootstrap/dist/js/bootstrap.min.js',
                    'cogenda_app/static/js/jquery.datatables/jquery.datatables.min.js',
                    'cogenda_app/static/js/jquery.quicksearch/jquery.quicksearch.js',
                    'cogenda_app/static/js/jquery.multiselect/js/jquery.multi-select.js',
                    'cogenda_app/static/js/jquery.select2/select2.min.js',
                    'cogenda_app/static/js/jquery.niftymodals/js/jquery.modalEffects.js',
                    'cogenda_app/static/js/jquery.quicksearch/jquery.quicksearch.js',
                    'cogenda_app/static/js/bootstrap.switch/bootstrap-switch.min.js',
                    'cogenda_app/static/js/jquery.parsley/2.0.0/parsley.js',
                    'cogenda_app/static/js/nprogress/nprogress.js',
                    'cogenda_app/static/js/i18n/zh_cn.js',
                    'cogenda_app/static/js/i18n/select2_locale_zh-CN.js',
                ],
                dest: 'cogenda_app/static/js/vendor.admin.js'
            },
            vendor_js_web: {
                src: [
                    'cogenda_app/static/js/jquery.js',
                    'cogenda_app/static/js/bxslider/jquery.bxslider.js',
                    'cogenda_app/static/js/bootstrap/dist/js/bootstrap.min.js',
                    'cogenda_app/static/js/jquery.parsley/2.0.0/parsley.js',
                    'cogenda_app/static/js/i18n/zh_cn.js',
                    'cogenda_app/static/js/nprogress/nprogress.js',
                    'cogenda_app/static/js/mediaelement/mediaelement-and-player.min.js',
                ],
                dest: 'cogenda_app/static/js/vendor.web.js'
            },
            vendor_css_admin: {
                src: [
                    'cogenda_app/static/js/bootstrap/dist/css/bootstrap.css',
                    'cogenda_app/static/js/font-awesome-4/css/font-awesome.min.css',
                    'cogenda_app/static/js/jquery.multiselect/css/multi-select.css',
                    'cogenda_app/static/js/jquery.select2/select2.css',
                    'cogenda_app/static/js/jquery.datatables/bootstrap-adapter/css/datatables.css',
                    'cogenda_app/static/js/jquery.niftymodals/css/component.css',
                    'cogenda_app/static/js/bootstrap.switch/bootstrap-switch.css',
                    'cogenda_app/static/js/nprogress/nprogress.css'
                ],
                dest: 'cogenda_app/static/css/vendor.admin.css'
            },
            vendor_css_web: {
                src: [
                    'cogenda_app/static/js/font-awesome-4/css/font-awesome.min.css',
                    'cogenda_app/static/js/bxslider/jquery.bxslider.css',
                    'cogenda_app/static/js/nprogress/nprogress.css',
                    'cogenda_app/static/js/mediaelement/mediaelementplayer.css'
                ],
                dest: 'cogenda_app/static/css/vendor.web.css'
            }
        },
        uglify: {
            dist: {
                files: {
                    'cogenda_app/static/js/cogenda.admin.min.js': ['cogenda_app/static/js/cogenda.admin.js'],
                    'cogenda_app/static/js/cogenda.web.min.js': ['cogenda_app/static/js/cogenda.web.js']
                    'cogenda_app/static/js/vendor.admin.min.js': ['cogenda_app/static/js/vendor.admin.js'],
                    'cogenda_app/static/js/vendor.web.min.js': ['cogenda_app/static/js/vendor.web.js']
                }
            }
        },
        cssmin: {
          minify: {
            expand: true,
            cwd: 'cogenda_app/static/css/',
            src: ['*.css', '!*.min.css'],
            dest: 'cogenda_app/static/css/',
            ext: '.min.css'
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
                    cwd: 'cogenda_app/static/images/',
                    src: '{,*/}*.{png,jpg,jpeg}',
                dest: 'cogenda_app/static/images/'
                }]
            }
        },
        clean: {
            dist: ['cogenda_app/static/css/cogenda.min.css', 'cogenda_app/static/js/cogenda.min.js']
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
            all: ['cogenda_app/static/js/cogenda.admin.js', 'cogenda_app/static/js/cogenda.web.js','!node_modules/**/*.js', '!test/**/*.js']
        }
    });

    // Load tasks
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-imagemin');
    grunt.loadNpmTasks('grunt-contrib-concat');

    // Register tasks
    grunt.registerTask('jslint', ['jshint']);
    grunt.registerTask('build', ['clean', 'recess', 'uglify', 'imagemin']);
    grunt.registerTask('inject', ['wiredep:web', 'wiredep:admin', 'wiredep:auth']);
};
