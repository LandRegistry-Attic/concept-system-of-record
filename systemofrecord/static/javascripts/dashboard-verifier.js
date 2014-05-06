(function() {
  window.LR = window.LR || {};

  var DashboardVerifier = LR.DashboardVerifier = function(options) {
    _.bindAll(this, 'fetchInvalidEntriesSuccess',
              'updateFromInvalidEntries');
    this.$el = $(options.el);
    this.startSpinner();
    this.setValid();
    this.fetchInvalidEntries();
  };

  DashboardVerifier.prototype = {
    fetchInvalidEntries: function() {
      console.log('Fetching invalid entries...')
      $.ajax({
        url: '/invalid-entries',
        success: this.fetchInvalidEntriesSuccess,
      });
    },
    fetchInvalidEntriesSuccess: function(result) {
      this.updateFromInvalidEntries(result.entries);
      this.fetchInvalidEntries();
    },
    updateFromInvalidEntries: function(entries) {
      console.log(entries.length+' invalid entries');
      if (entries.length === 0) {
        this.setValid();
      }
      else {
        this.setInvalid(entries);
      }
    },
    startSpinner: function() {
      var spinner = new Spinner().spin();
      this.$el.find('.spinner').append(spinner.el);
    },
    setValid: function() {
      this.$el.find('.status-text').text('All records intact')
      this.$el.find('.big-icon')
        .removeClass('glyphicon-remove')
        .addClass('glyphicon-ok');
    },
    setInvalid: function(entries) {
      if (entries.length == 1) {
        var statusText = '1 record is incorrect';
      }
      else {
        var statusText = entries.length + ' records are incorrect';
      }
      this.$el.find('.status-text').text(statusText);
      this.$el.find('.big-icon')
        .removeClass('glyphicon-ok')
        .addClass('glyphicon-remove');
    }
  };
})();
