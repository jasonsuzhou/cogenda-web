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
                    'cogenda_app/static/vendor/jquery.js',
                    'cogenda_app/static/vendor/jquery-ui.js',
                    'cogenda_app/static/vendor/bootstrap/dist/js/bootstrap.min.js',
                    'cogenda_app/static/vendor/jquery.datatables/jquery.datatables.min.js',
                    'cogenda_app/static/vendor/jquery.quicksearch/jquery.quicksearch.js',
                    'cogenda_app/static/vendor/jquery.multiselect/js/jquery.multi-select.js',
                    'cogenda_app/static/vendor/jquery.select2/select2.min.js',
                    'cogenda_app/static/vendor/jquery.niftymodals/js/jquery.modalEffects.js',
                    'cogenda_app/static/vendor/jquery.quicksearch/jquery.quicksearch.js',
                    'cogenda_app/static/vendor/bootstrap.switch/bootstrap-switch.min.js',
                    'cogenda_app/static/vendor/jquery.parsley/2.0.0/parsley.js',
                    'cogenda_app/static/vendor/nprogress/nprogress.js',
                    'cogenda_app/static/vendor/i18n/zh_cn.js',
                    'cogenda_app/static/vendor/i18n/select2_locale_zh-CN.js'
                ],
                dest: 'cogenda_app/static/js/vendor.admin.js'
            },
            vendor_js_auth: {
                src: [
                    'cogenda_app/static/vendor/jquery.js',
                    'cogenda_app/static/vendor/jquery.parsley/2.0.0/parsley.js',
                    'cogenda_app/static/vendor/i18n/zh_cn.js',
                    'cogenda_app/static/vendor/nprogress/nprogress.js',
                    'cogenda_app/static/vendor/bootstrap/dist/js/bootstrap.min.js'
                ],
                dest: 'cogenda_app/static/js/vendor.auth.js'
            },
            vendor_js_web: {
                src: [
                    'cogenda_app/static/vendor/jquery.js',
                    'cogenda_app/static/vendor/bxslider/jquery.bxslider.js',
                    'cogenda_app/static/vendor/bootstrap/dist/js/bootstrap.min.js',
                    'cogenda_app/static/vendor/jquery.parsley/2.0.0/parsley.js',
                    'cogenda_app/static/vendor/i18n/zh_cn.js',
                    'cogenda_app/static/vendor/nprogress/nprogress.js',
                    'cogenda_app/static/vendor/mediaelement/mediaelement-and-player.min.js'
                ],
                dest: 'cogenda_app/static/js/vendor.web.js'
            },
            vendor_css_admin: {
                src: [
                    'cogenda_app/static/vendor/bootstrap/dist/css/bootstrap.css',
                    'cogenda_app/static/vendor/font-awesome-4/css/font-awesome.min.css',
                    'cogenda_app/static/vendor/jquery.multiselect/css/multi-select.css',
                    'cogenda_app/static/vendor/jquery.select2/css/select2.css',
                    'cogenda_app/static/vendor/jquery.datatables/bootstrap-adapter/css/datatables.css',
                    'cogenda_app/static/vendor/jquery.niftymodals/css/component.css',
                    'cogenda_app/static/vendor/bootstrap.switch/bootstrap-switch.css',
                    'cogenda_app/static/vendor/nprogress/nprogress.css'
                ],
                dest: 'cogenda_app/static/css/vendor-admin.css'
            },
            vendor_css_web: {
                src: [
                    'cogenda_app/static/vendor/font-awesome-4/css/font-awesome.min.css',
                    'cogenda_app/static/vendor/bxslider/css/jquery.bxslider.css',
                    'cogenda_app/static/vendor/nprogress/nprogress.css',
                    'cogenda_app/static/vendor/mediaelement/mediaelementplayer.css'
                ],
                dest: 'cogenda_app/static/css/vendor-web.css'
            }
        },
        uglify: {
            dist: {
                files: {
                    'cogenda_app/static/js/cogenda.admin.min.js': ['cogenda_app/static/js/cogenda.admin.js'],
                    'cogenda_app/static/js/cogenda.web.min.js': ['cogenda_app/static/js/cogenda.web.js'],
                    'cogenda_app/static/js/vendor.admin.min.js': ['cogenda_app/static/js/vendor.admin.js'],
                    'cogenda_app/static/js/vendor.auth.min.js': ['cogenda_app/static/js/vendor.auth.js'],
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
        copy: {
            main: {
                files: [
                    // copy vendor lib fonts
                    {expand: true, flatten: true, cwd:'cogenda_app/static/vendor', src: ['bootstrap/dist/fonts/*', 'font-awesome-4/fonts/*'], dest: 'cogenda_app/static/fonts/', filter: 'isFile'},
                    // copy vendor lib images
                    {expand: true, flatten: true, cwd:'cogenda_app/static/vendor', src: ['bxslider/images/*', 'jquery.datatables/bootstrap-adapter/images/*', 'jquery.multiselect/images/*', 'jquery.select2/images/*','mediaelement/*.{png,gif}' ], dest: 'cogenda_app/static/images/', filter: 'isFile'},
                    // copy vendor lib misc
                    {expand: true, flatten: true, src: ['cogenda_app/static/vendor/mediaelement/*.swf'], dest: 'cogenda_app/static/media/', filter: 'isFile'},
                ]
            }
        },
        imagemin: {
            dist: {
                options: {
                    optimizationLevel: 3,
                    progressive: true
                },
                files: [{
                    expand: true,
                    cwd: 'cogenda_app/static/images/',
                    src: ['{,*/}*.{jpg,jpeg,gif}'],
                    dest: 'cogenda_app/static/images/'
                }]
            }
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
        },
        clean: {
            pre_build: [
                'cogenda_app/static/css/*.min.css',
                'cogenda_app/static/css/vendor-admin.css',
                'cogenda_app/static/css/vendor-web.css',
                'cogenda_app/static/js/*.min.js',
                'cogenda_app/static/js/vendor.admin.js',
                'cogenda_app/static/js/vendor.auth.js',
                'cogenda_app/static/js/vendor.web.js'
            ],

            post_build: [
                'cogenda_app/static/css/vendor-admin.css',
                'cogenda_app/static/css/vendor-web.css',
                'cogenda_app/static/js/vendor.admin.js',
                'cogenda_app/static/js/vendor.auth.js',
                'cogenda_app/static/js/vendor.web.js'
            ]
        }
    });

    // Load tasks
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-imagemin');
    grunt.loadNpmTasks('grunt-contrib-concat');

    // Register tasks
    grunt.registerTask('jslint', ['jshint']);
    grunt.registerTask('build', ['clean:pre_build', 'concat', 'uglify', 'cssmin', 'copy', 'imagemin', 'clean:post_build']);
};
