(function() {
  window.LR = window.LR || {};

  var DashboardVerifier = LR.DashboardVerifier = function(options) {
    _.bindAll(this,
      'fetchInvalidEntries',
      'fetchInvalidEntriesSuccess',
      'updateFromInvalidEntries'
    );
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
      setTimeout(this.fetchInvalidEntries, 5000);
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
      this.$el.find('.altered-records').html('');
      this.$el.find('.big-icon')
        .removeClass('glyphicon-remove')
        .addClass('glyphicon-ok');
    },
    setInvalid: function(entries) {
      if (entries.length == 1) {
        var statusText = '1 record has been altered';
      }
      else {
        var statusText = entries.length + ' records are incorrect';
      }
      this.$el.find('.status-text').text(statusText);


      var $table = $('<table class="table"><thead><tr><th>Version</th><th>Title number</th><th>Address</th></tr></thead><tbody></tbody></table>');

      var rowTemplate = _.template('<tr><td><%- id %></td><td><%- title_number %></td><td><%- address %></td>');

      _.each(entries, function(entry) {
        $table.find('tbody').append(rowTemplate({
          id: entry.id.slice(0, 16) + '...',
          title_number: entry.content.title_number,
          address: entry.content.address,
        }));
      });
      var entry = entries[0];
      this.$el.find('.altered-records').append('<p>'+entry.content.title_number+'</p>')
      this.$el.find('.altered-records').html($table);


      this.$el.find('.big-icon')
        .removeClass('glyphicon-ok')
        .addClass('glyphicon-remove');
    }
  };
})();
