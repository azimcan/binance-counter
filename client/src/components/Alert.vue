<template>
  <div>
    <div class="alert alert-success alert-dismissible fade show" role="alert">
      {{ message }}
      <button class="btn-close"
              type="button"
              data-bs-dismiss="alert"
              aria-label="Close"
              @click="closeAlert()">
      </button>
    </div>
    <br>
  </div>
</template>

<script>
export default {
  props: {
    message: String,
    showMessage: Boolean,
  },
  methods: {
    closeAlert() {
      this.$emit('closeAlert');
    },
  },
};
</script>
