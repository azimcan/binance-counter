<template>
  <div class="container">
      <h1>Symbols</h1>
      <hr><br><br>
      <alert :message=message v-if="showMessage"></alert>
      <div class="d-flex justify-content-left">
        <b-form @submit="onSubmit">
          <label class="sr-only mb-2" for="form-input-name">Symbol</label>
          <div class="input-group">
            <b-form-input
              id="form-title-input"
              type="text"
              v-model="addSymbolForm.symbol"
              required
              placeholder="BTC"
              style="text-transform: uppercase;"
            ></b-form-input>
            <b-button type="submit" variant="success">Add Symbol</b-button>
          </div>
        </b-form>
      </div>

      <br><br>
      <table class="table table-hover">
        <thead>
          <tr>
            <th scope="col">Symbol</th>
            <th scope="col">Currency Pair</th>
            <th scope="col">Average Buy</th>
            <th scope="col">Average Sell</th>
            <th scope="col">Executed Buy</th>
            <th scope="col">Executed Sell</th>
            <th scope="col">Global Average</th>
            <th scope="col">Net Executed</th>
            <th scope="col">Profit</th>
            <th scope="col">Commission</th>
            <th scope="col">Step Size</th>
            <th scope="col">Tick Size</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(symbol, index) in symbols" :key="index">
            <td>{{ symbol.symbol }}</td>
            <td>{{ symbol.currency_pair }}</td>
            <td>{{ symbol.average_buy }}</td>
            <td>{{ symbol.average_sell }}</td>
            <td>{{ symbol.executed_buy }}</td>
            <td>{{ symbol.executed_sell }}</td>
            <td>{{ symbol.global_average }}</td>
            <td>{{ symbol.net_executed }}</td>
            <td>{{ symbol.profit }}</td>
            <td>{{ symbol.commission }}</td>
            <td>{{ symbol.step_size }}</td>
            <td>{{ symbol.tick_size }}</td>
            <!-- <td>
              <span v-if="book.read">Yes</span>
              <span v-else>No</span>
            </td> -->
            <td>
              <div class="btn-group" role="group">
                <button type="button" class="btn btn-danger btn-sm"
                        @click="onDeleteSymbol(symbol)">Delete</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
  </div>
</template>

<script>

import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      symbols: [],
      addSymbolForm: {
        symbol: '',
      },
      messsage: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getSymbols() {
      const path = 'http://localhost:5000/symbols';
      axios.get(path)
        .then((res) => {
          this.symbols = res.data.symbols;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addSymbol(payload) {
      const path = 'http://localhost:5000/symbols';
      // eslint-disable-next-line
      console.log(payload)
      axios.post(path, payload)
        .then(() => {
          this.getSymbols();
          this.message = 'Symbol added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getSymbols();
        });
    },
    removeSymbol(symbolID) {
      const path = `http://localhost:5000/symbols/${symbolID}`;
      axios.delete(path)
        .then(() => {
          this.getSymbols();
          this.message = 'Symbol removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getSymbols();
        });
    },
    initForm() {
      this.addSymbolForm.symbol = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      const payload = {
        symbol: this.addSymbolForm.symbol.toUpperCase(),
      };
      this.addSymbol(payload);
      this.initForm();
    },
    onDeleteSymbol(symbol) {
      this.removeSymbol(symbol.symbol);
    },
  },
  created() {
    this.getSymbols();
  },
};
</script>
