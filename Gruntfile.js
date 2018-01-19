var staticPathPrefix = 'static',
    proxyUrl = 'localhost:8000';
    
module.exports = function (grunt) {
    grunt.initConfig({
        watch: {
            files: 'sass/**/*.{scss,sass}',
            tasks: ['sass']
        },
        sass: {
            dist: {
                files: {
                    'static/css/warmpi.css': 'sass/manifest.scss'
                }
            }
        },

        browserSync: {
            dev: {
                bsFiles: {
                    src : [
                        staticPathPrefix + '/css/*.css',
                        staticPathPrefix + '/js/*.js',
                        '**/*.py'
                    ]
                },
                options: {
                    watchTask: true,
                    proxy: proxyUrl,
                    online: true
                }
            }
        },
        shell: {
            flaskRun: {
                command: '/bin/bash -c "env/bin/python manage.py runserver"',
                options: {
                  stdout: true,
                  failOnError: true,
                  async: true
                }
            }
        }
    });

    // load npm tasks
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-browser-sync');
    grunt.loadNpmTasks('grunt-shell-spawn');

    // define default task
    grunt.registerTask('default', ['shell:flaskRun', 'browserSync', 'watch']);
};
