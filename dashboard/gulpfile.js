/**
 * Created by Afonso on 24/05/2015.
 */
var gulp = require('gulp');
var sass = require('gulp-sass');
var watch = require('gulp-watch');
var livereload = require('gulp-livereload');

/* Compile Our Sass */
gulp.task('sass', function() {
    return gulp.src('static/network/scss/*.scss')
        .pipe(sass())
        .pipe(gulp.dest('static/network/css'))
        .pipe(livereload());
});

/* Watch Files For Changes */
gulp.task('watch', function() {
    livereload.listen();
    gulp.watch('static/network/scss/**/*.scss', ['sass']);

    /* Trigger a live reload on any Django template changes */
    gulp.watch('**/templates/*').on('change', livereload.changed);

});

gulp.task('default', ['sass', 'watch']);

